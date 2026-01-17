from dotenv import load_dotenv
load_dotenv()

from livekit.agents import AgentSession, Agent, JobContext, WorkerOptions, cli
from livekit.plugins import silero, deepgram, openai
from livekit.plugins.elevenlabs import TTS
import os

async def entrypoint(ctx: JobContext):
    await ctx.connect()

    agent = Agent(instructions="Say something long.")

    session = AgentSession(
        vad=silero.VAD.load(),
        stt=deepgram.STT(model="nova-3"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=TTS(
            api_key=os.environ["ELEVENLABS_API_KEY"],
            voice_id="CwhRBWXzGAHq8TQ4Fs17",
            model="eleven_turbo_v2",
        ),
    )

    @session.on("agent_state_changed")
    def on_agent_state_changed(ev):
        print(f"[AGENT_STATE] {ev.old_state} -> {ev.new_state}")

    await session.start(agent=agent, room=ctx.room)

    print("Calling session.say()")
    await session.say(
        "This is a very long sentence that should obviously count as speech "
        "if audio playback were actually happening."
    )
    print("session.say() finished")

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
