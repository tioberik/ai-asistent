import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=KEY)

# --------------------------------------------------------------
# Upload file
# --------------------------------------------------------------
def upload_file(path):
    # Upload a file with an "assistants" purpose
    file = client.files.create(file=open(path, "rb"), purpose="assistants")
    return file


file = upload_file("../data/upute.pdf")


# --------------------------------------------------------------
# Create assistant
# --------------------------------------------------------------
def create_assistant(file):
    """
    You currently cannot set the temperature for Assistant via the API.
    """
    assistant = client.beta.assistants.create(
        name="eDnevnik virtualni asistent",
        instructions="Ti si virtualni pomoćnik koji pomaže nastavnicima osnovnih i srednjih škola koje rade nastavu po hrvatskom planu i programu u Bosni i Hercegovini pri radu sa aplikacijom e-Dnevnik. Svoje znanje dohvaćaš iz priloženih materijala (upute.pdf) gdje su sastavljene upute o radu eDnevnika. Odgovori moraju biti na književnom hrvatskom jeziku, te moraju biti direktni i uobličeni na način da su lako razumljivi čak i osobama koje nemaju puno iskustva ori radu s računalom. Ako ne znaš odgovor, jednostavno reci da ne možeš pomoći i savjetuj ih da kontaktiraju SUMIT korisničku podršku. Budi ljubazan.",
        tools=[{"type": "retrieval"}],
        model="gpt-4-1106-preview",
        file_ids=[file.id],
    )
    return assistant


assistant = create_assistant(file)

#-------------------------------

print(create_assistant().id)
