"use server"

import { openai } from "@/lib/openai"

export const transcribe = async (data: Blob) => {
  const { text } = await openai.audio.transcriptions.create({
    file: new File([data], "audio.ogg"),
    model: "whisper-1",
  })

  console.log(text)
}
