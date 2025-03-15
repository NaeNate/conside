"use client"

import { useRef, useState } from "react"

export default function Home() {
  const chunks = useRef<Blob[]>([])
  const [text, setText] = useState("")

  return (
    <>
      <h1>Conside</h1>

      <button
        onClick={() => {
          const record = async () => {
            const recorder = new MediaRecorder(
              await navigator.mediaDevices.getUserMedia({ audio: true }),
              { mimeType: "audio/webm" },
            )

            recorder.ondataavailable = (e) => {
              chunks.current.push(e.data)
            }

            recorder.onstop = async () => {
              const audio = new Blob(chunks.current, { type: "audio/webm" })
              chunks.current = []

              const fd = new FormData()
              fd.append("audio", audio)

              const x = await fetch("http://localhost:8000/api/transcribe", {
                method: "POST",
                body: fd,
              }).then((res) => res.json())

              setText((prev) => prev + x.claim)
              console.log(x)

              recorder.start()
              setTimeout(() => recorder.stop(), 5000)
            }

            recorder.start()
            setTimeout(() => recorder.stop(), 5000)
          }

          record()
        }}
      >
        Go
      </button>

      {text}
    </>
  )
}
