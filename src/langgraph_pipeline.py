from typing import Dict, Any
from langgraph.graph import StateGraph, START, END
from src.weather import fetch_weather_by_city
from src.rag import answer_question
from src.langsmith_eval import run_langsmith_evaluation
from src.config import Config

def desicion_node(state: Dict[str, Any], *_, **__):
    """
    Expect `state` to include 'input' with user's text.
    Decision logic:
      - if input contains 'weather' or 'temperature' -> choose weather
      - else -> choose pdf_rag
    """
    text_l = state['input'].lower()
    weather_terms = ['weather', 'wheather', 'temperature', 'forecast', 'humidity', 'rain', 'wind', 'climate']
    if any(kw in text_l for kw in weather_terms):
        state["action"] = "weather"
    else:
        state["action"] = "pdf_rag"
    return state

def weather_node(state: Dict[str, Any]):

    # parse city from input, default to Config.DEFAULT_CITY

    text = state.get('input', "")

    # naive extraction of city name

    city = None
    parts = text.lower().split("in ")
    if len(parts) > 1:
        city = parts[-1].strip().split("?")[0]
    
    city = city or Config.DEFAULT_CITY

    weather = fetch_weather_by_city(city)

    state["weather_result"] = weather
    observed = weather.get('observation_time')
    observed_text = f" Observed at {observed}." if observed else ""
    state["final"] = (
        f"The weather in {weather['city']}, {weather['country']} is {weather['description']} "
        f"with a temperature of {weather['temperature']}°C, humidity at {weather['humidity']}% "
        f"and wind speed of {weather['wind_speed']} m/s.{observed_text}"
    )
    return state

def pdf_rag_node(state: Dict[str, Any]):
    question = state.get('input', "")
    rag_response = answer_question(question)
    state["rag_response"] = rag_response
    state["final"] = rag_response['result'] if isinstance(rag_response, dict) else str(rag_response)
    return state

def llm_postprocess_node(state: Dict[str, Any]):
    # for now, just pass through the final result
    return state

def build_graph():
    sg = StateGraph(dict)
    sg.add_node("desicion", desicion_node)
    sg.add_node("weather", weather_node)
    sg.add_node("pdf_rag", pdf_rag_node)
    sg.add_node("llm_postprocess", llm_postprocess_node)

    sg.add_edge(START, "desicion")

    def route(state: Dict[str, Any]):
        return "weather" if state.get("action") == "weather" else "pdf_rag"

    sg.add_conditional_edges("desicion", route)
    sg.add_edge("weather", "llm_postprocess")
    sg.add_edge("pdf_rag", "llm_postprocess")
    sg.add_edge("llm_postprocess", END)

    return sg.compile()

def run_pipeline(user_input: str):
    graph = build_graph()
    initial_state = {"input": user_input}
    final_state = graph.invoke(initial_state)
    return final_state

