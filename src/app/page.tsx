"use client"

import { useEffect, useState } from "react"
import { transcribe } from "./actions"

export default function Home() {
  const [recorder, setRecorder] = useState<MediaRecorder>()

  useEffect(() => {
    navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
      const rec = new MediaRecorder(stream)

      rec.ondataavailable = async ({ data }) => {
        await transcribe(data)
      }

      setRecorder(rec)
    })
  }, [])

  const start = () => {
    if (recorder) recorder.start(2000)
  }

  const stop = () => {
    if (recorder) recorder.stop()
  }

  return (
    <>
      <button onClick={start}>Start</button>
      <button onClick={stop}>Stop</button>
    </>
  )
}
