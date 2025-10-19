import React, { useState } from "react";

const FieldLabel = ({ children, required = false }) => (
  <label className="text-xs tracking-wide text-zinc-300 uppercase select-none">
    {children}
    {required && <span className="text-lime-400"> *</span>}
  </label>
);

const DurationControl = ({ value, setValue, min = 5, max = 120, step = 5 }) => {
  const clamp = (n) => Math.min(max, Math.max(min, Number.isFinite(n) ? n : min));
  return (
    <div className="space-y-2 opacity-50">
      <FieldLabel required>DURATION (seconds)</FieldLabel>
      <div className="flex items-center gap-3">
        <input
          type="range"
          min={min}
          max={max}
          step={step}
          value={value}
          onChange={(e) => setValue(clamp(parseInt(e.target.value, 10)))}
          className="flex-1 accent-lime-400"
        />
        <input
          type="number"
          min={min}
          max={max}
          step={step}
          value={value}
          onChange={(e) => setValue(clamp(parseInt(e.target.value, 10)))}
          className="w-20 sm:w-24 rounded-lg bg-zinc-900/70 border border-zinc-700/70 px-3 py-2 text-zinc-200 focus:outline-none focus:ring-2 focus:ring-lime-400/60"
        />
      </div>
    </div>
  );
};

export default function ConSuo() {
  const [prompt, setPrompt] = useState("");
  const [duration, setDuration] = useState(5);
  const [output, setOutput] = useState(null);

  function handleGenerate() {
    const payload = { engine: "", prompt, duration_seconds: duration };
    setTimeout(() => setOutput(JSON.stringify(payload, null, 2)), 120);
  }

  function handleReset() {
    setPrompt("");
    setDuration(5);
    setOutput(null);
  }

  return (

    <div className="min-h-screen w-full bg-[#0b0c0f] text-zinc-100 flex flex-col">

      <div className="flex-1">
        <div className="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8 py-6 lg:py-10">
          <main className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6 lg:gap-8">
            {/* Left panel */}
            <section className="rounded-xl border border-zinc-800 bg-black/30 p-4 sm:p-5 md:p-6">
              <h2 className="mb-4 text-sm font-bold tracking-wide text-zinc-300">Consuo</h2>

              <div className="space-y-2 opacity-50">
                <FieldLabel required>PROMPT</FieldLabel>
                <textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="Describe the scene you want to generate…"
                  className="w-full resize-y rounded-lg bg-zinc-900/70 border border-zinc-700/70 px-3 py-3 text-zinc-200 placeholder:text-zinc-500 focus:outline-none focus:ring-2 focus:ring-lime-400/60 min-h-[160px] sm:min-h-[200px] md:min-h-[260px]"
                />
              </div>

              <div className="mt-6">
                <DurationControl value={duration} setValue={setDuration} min={5} max={120} step={5} />
              </div>

              <div className="mt-6 flex flex-col-reverse sm:flex-row sm:justify-end gap-2">
                <button
                  onClick={handleReset}
                  className="w-full sm:w-auto inline-flex items-center justify-center gap-2 rounded-lg bg-zinc-800 px-4 py-2 text-sm font-medium text-zinc-200 border border-zinc-700 hover:bg-zinc-700/60 focus:outline-none focus:ring-2 focus:ring-zinc-500/50"
                >
                  ⟳ Reset
                </button>
                <button
                  onClick={handleGenerate}
                  className="w-full sm:w-auto inline-flex items-center justify-center gap-2 rounded-lg bg-lime-400 px-4 py-2 text-sm font-semibold text-black shadow hover:brightness-95 focus:outline-none focus:ring-2 focus:ring-lime-400/70"
                >
                  Generate
                </button>
              </div>
            </section>

            <section className="rounded-xl border border-zinc-800 bg-black/30 p-4 sm:p-5 md:p-6 min-h-[340px] sm:min-h-[420px] md:min-h-[560px] flex flex-col">
              <div className="mb-2 text-sm text-zinc-200/50">Output</div>
              <div className="flex-1 rounded-lg border border-zinc-800 bg-zinc-950/50 p-4 overflow-auto">
                {output ? (
                  <pre className="text-xs leading-relaxed text-zinc-200 whitespace-pre-wrap break-words">{output}</pre>
                ) : (
                  <div className="h-full grid place-items-center text-zinc-500 text-sm text-center">
                    Output will appear here after generation
                  </div>
                )}
              </div>
            </section>
          </main>
        </div>
      </div>

      <footer className="w-full bg-lime-400 text-black">
        <div className="mx-auto max-w-7xl px-4 sm:px-8 py-5 grid grid-cols-1 sm:grid-cols-2 items-center gap-4">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <img
              src="/icon.png"  
              alt="Higgsfield"
              className="h-7 sm:h-8 w-auto"
            />
            <span className="font-semibold tracking-tight"></span>
          </div>
          {/* Contact */}
          <ul className="flex flex-wrap items-center justify-start sm:justify-end gap-x-6 gap-y-1 text-sm sm:text-[13px]">
            <li>
              <a href="mailto:contact@higgsfield.com" className="hover:underline hover:opacity-80 transition-opacity">
                mikhail.yurikov@nu.edu.kz
              </a>
            </li>
            <li>
              <a href="tel:+14155551234" className="hover:underline hover:opacity-80 transition-opacity">
                +7 776 310 10 05
              </a>
            </li>
            <li className="opacity-80">Daily Cup, Nazarbayev University, Astana, Kazakhstan</li>
          </ul>
        </div>
      </footer>
    </div>
  );
}
