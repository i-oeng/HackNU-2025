# app.py (minimal serial Soul generation)
import os
import time
import asyncio
import requests
from typing import List, Dict, Any
from fastapi import FastAPI, Query
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("HF_API_BASE", "https://platform.higgsfield.ai/v1")
HEADERS = {
    "hf-api-key": os.environ["HF_API_KEY"],
    "hf-secret":  os.environ["HF_SECRET"],
    "Content-Type": "application/json",
    "Accept": "application/json"
}

POLL_INTERVAL_S = 2.0
POLL_TIMEOUT_S  = 600.0

app = FastAPI()

import os, subprocess

def concat_videos(video_paths, output_path="final_videos/final_output.mp4"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    list_path = "concat_list.txt"
    with open(list_path, "w") as f:
        for v in video_paths:
            f.write(f"file '{os.path.abspath(v)}'\n")

    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_path,
        "-c", "copy",  
        output_path,
    ]

    print(f"[FFMPEG] Combining {len(video_paths)} clips → {output_path}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError("FFmpeg concat failed")

    os.remove(list_path)

    return os.path.abspath(output_path)


def prompt_divider(prompt: str, num: int) -> List[str]:
    words = prompt.split()
    if num <= 1 or len(words) <= 1:
        return [prompt]
    base = len(words) // num
    rem  = len(words) % num
    out: List[str] = []
    i = 0
    for k in range(num):
        take = base + (1 if k < rem else 0)
        if take <= 0: 
            continue
        out.append(" ".join(words[i:i+take]))
        i += take
    if len(out) == 1:
        out.append(out[0])
    return out

def extract_first_url(jobset: Dict[str, Any]) -> str:
    for job in jobset.get("jobs", []):
        res = job.get("results") or {}
        url = (res.get("raw") or {}).get("url") or (res.get("min") or {}).get("url") or ""
        if url:
            return url
    return ""

def download_image(url: str, save_dir: str, index: int) -> str:
    os.makedirs(save_dir, exist_ok=True)
    ext = ".png"
    for cand in (".png", ".jpg", ".jpeg", ".webp"):
        if cand in url.lower():
            ext = cand
            break
    path = os.path.join(save_dir, f"img_{index:04d}{ext}")
    with requests.get(url, headers=HEADERS, stream=True, timeout=(10, 120)) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)
    return path

@app.post("/")
async def generate(
    prompt: str = Query("A spontaneous candid image of a female model with sharp eyes and porcelain skin sitting naturally on a minimalist white metal bench in a sculptural desert garden, wearing a crisp sand-colored suit featuring a boxy silhouette and square-toed boots. The late afternoon sunlight casts soft, warm natural lighting across her skin and the fabric'\''s fine texture, highlighting subtle shadows and natural imperfections. Her relaxed, minimally aware expression and casual posture evoke genuine intimacy, while the surrounding desert plants and sculptural elements add authentic environmental detail. The composition is casually tilted and framed to emphasize spontaneous realism, characteristic of high-quality iPhone photography with natural depth and texture."),
    width_and_height: str = Query("2048x1152"),
    duration: int = Query(15),
):
    num = max(1, duration // 5)
    parts = prompt_divider(prompt, num)


    saved_urls: List[str] = []
    saved_paths: List[str] = []
    results: List[Dict[str, Any]] = []
    prompt_now = ""

    for i, p in enumerate(parts):
        try:
            prompt_now += " " + p
            params: Dict[str, Any] = {
                "prompt": prompt_now + ". Generate the last action from the sentences before that one.",
                "width_and_height": width_and_height,
                "enhance_prompt": False,
                "batch_size": 1,
                "seed": 500000,
                "style_id": "1cb4b936-77bf-4f9a-9039-f3d349a4cdbe",
                "custom_reference_id": "3eb3ad49-775d-40bd-b5e5-38b105108780"
            }
            if saved_urls: 
                params["image_reference"] = {
                    "type": "image_url",
                    "image_url": saved_urls[-1],
                }

            payload = {"params": params}

            r = requests.post("https://platform.higgsfield.ai/v1/text2image/nano_banana", json=payload, headers=HEADERS, timeout=(10, 60))
            r.raise_for_status()
            js = r.json()
            job_set_id = js.get("id") or js.get("job_set_id")
            if not job_set_id:
                raise RuntimeError(f"No job_set_id in response: {js}")

            start = time.monotonic()
            while True:
                g = requests.get(f"{URL}/job-sets/{job_set_id}", headers=HEADERS, timeout=(10, 30))
                g.raise_for_status()
                jset = g.json()
                jobs = jset.get("jobs") or []
                if jobs and all(j.get("status") in {"completed","failed","canceled"} for j in jobs):
                    break
                if time.monotonic() - start > POLL_TIMEOUT_S:
                    raise TimeoutError(f"Timeout for {job_set_id}")
                await asyncio.sleep(POLL_INTERVAL_S)

            url = extract_first_url(jset)
            if not url:
                results.append({"index": i, "prompt": prompt_now , "error": "no result url"})
                continue


            saved_urls.append(url)
            results.append({"index": i, "prompt": p, "url": url})

        except requests.HTTPError as e:
            print(f"[HTTP ERROR] {e}")
            print("[RESPONSE BODY]", r.text)
            results.append({
                "index": i,
                "prompt": prompt_now,
                "error": f"HTTPError: {e}",
                "body": r.text
            })
            continue

#----------------------Image_To_Video-----------------

        params: Dict[str, Any] = {
            "model": "dop-turbo",
            "prompt": "<string>",
            "seed": 500000,
            "motions": [
              {
                "id": "3c90c3cc-0d44-4b50-8888-8dd25736052a",
                "strength": 0.5
              }
            ],
            "input_images": [
              {
                "type": "image_url",
                "image_url": "<string>"
              }
            ],
            "input_images_end": [
              {
                "type": "image_url",
                "image_url": "<string>"
              }
            ],

        }
        prompt_now = parts[0]
        for i in range(1,saved_urls):
            prompt_now += " " + parts[i]
            params["prompt"] = prompt_now
            params["input_images"]["image_url"] = saved_urls[i-1]
            params["input_images_end"]["image_url"]=save_urls[i]
            payload["params"] = params
            r = requests.post("{url}/image2video/dop", json=payload, headers=HEADERS, timeout=(10, 300))
            video_id = r["jobs"]["id"]
            v = requests.get("{url}/job-sets/{video_id}", headers=HEADERS)
            url = extract_first_url(v)
            local_path = os.path.join("videos", f"seg_{i-1:04d}{ext}")
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with requests.get(url, headers=HEADERS, stream=True, timeout=(10,300)) as r:
                r.raise_for_status()
                with open(local_path, "wb") as f:
                    for chunk in r.iter_content(1024 * 1024):
                        if chunk: f.write(chunk)

            final_path = concat_videos(videos, output_path="final_videos/my_demo.mp4")



    return {
        "parts": parts,
        "results": results,
        "saved_paths": saved_paths,
    }
