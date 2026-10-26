"""Single-file AutoGen HR assistant with Streamlit UI and Console output."""
import asyncio
import os

from dotenv import load_dotenv
import streamlit as st
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

SYSTEM_MESSAGE = "You are an HR assistant."
DEFAULT_REQUEST = "Write exactly 5 lines of a job description for a Junior Python Developer."


async def generate_description(request: str) -> str:
    """Run AutoGen, print the streamed response, and close the client."""
    model_client = OpenAIChatCompletionClient(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        api_key=os.environ["OPENAI_API_KEY"],
    )
    try:
        agent = AssistantAgent(
            name="hr_assistant",
            system_message=SYSTEM_MESSAGE,
            model_client=model_client,
        )
        # Console consumes the stream and prints messages in the terminal.
        result = await Console(agent.run_stream(task=request))
        for message in reversed(result.messages):
            if message.source == agent.name:
                return str(message.content)
        raise RuntimeError("The HR assistant returned no reply.")
    finally:
        await model_client.close()


def main() -> None:
    st.set_page_config(page_title="AutoGen HR Assistant", page_icon="💼")
    st.title("💼 AutoGen HR Assistant")
    st.caption("Generate a job description using AutoGen and OpenAI.")
    request = st.text_area("HR request", value=DEFAULT_REQUEST, height=110)
    if st.button("Generate job description", type="primary"):
        if not os.getenv("OPENAI_API_KEY"):
            st.error("Set OPENAI_API_KEY in your .env file or environment before running the app.")
        elif not request.strip():
            st.warning("Enter an HR request.")
        else:
            with st.spinner("Generating..."):
                try:
                    reply = asyncio.run(generate_description(request.strip()))
                except Exception as exc:
                    st.error(f"Generation failed: {exc}")
                else:
                    st.subheader("Job description")
                    st.text(reply)
                    st.download_button("Download as TXT", reply, file_name="junior_python_developer_jd.txt")


if __name__ == "__main__":
    main()
