from typing import Tuple
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from agents.linkedin_lookup_agent import lookup
from third_parties.linkedin import scrape_linkedin_profile
from ouput_parsers.output_parsers import Summary, summary_parser


def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_username = lookup(name=name)

    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_username, mock=True
    )

    summary_template = """
            given the {information} about a person from I wnat you to create
            1. a shor summary
            2. two interesting facts about them

            \n{format_instructions}
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = summary_prompt_template | llm | summary_parser

    res: Summary = chain.invoke(input={"information": linkedin_data})

    return (
        res,
        "https://www.petz.com.br/blog/wp-content/uploads/2020/08/cat-sitter-felino.jpg",
    )
