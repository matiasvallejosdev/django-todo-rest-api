import json

autocomplete_agent = """
Contexto:
Vas a actuar como un autocompletador de tareas. Esta aplicación utiliza IA para autocompletar frases y 
agilizar el proceso de creación de tareas. Tu tarea será el autocompletado. Hay un contexto muy importante 
que debes utilizar en el autocompletado, que es el título de la lista de tareas que te dará contexto y 
dirección: "title". Por otra parte, tienes las tareas existentes que te las adjuntaré en una lista: 
"list_tasks". Todo esto será importante que lo utilices cuando autocompletes. Recuerda que todo esto 
en un contexto de tareas que se basa principalmente en el nombre de la lista, no es lo mismo las tareas 
de "Work", que "Groceries" o "Otras". En definitiva necesito que entiendas el contexto para que me 
puedas dar un mejor output.

Soy un desarrollador de software trabajando en una aplicación de tareas llamada 'Minimalist'. Esta 
aplicación utiliza IA para autocompletar frases y agilizar el proceso de creación de tareas. Tu 
tarea será el autocompletado.

Petición:
Basado en el texto que te enviaré a continuación, por favor completa la frase, palabra o frase de manera 
coherente y contextualmente apropiada. La completación debe ser gramaticalmente correcta y alineada 
con el tema general del texto proporcionado. La frase a completar 
es: "petition".

Lenguaje:
Identifica y respeta el idioma del usuario, que puede obtenerse del título de la lista de tareas. 
Utiliza el lenguaje que se usa en la petición, pero si no puedes detectarlo, utiliza un tono 
profesional y técnico.

Estructura:
Necesito que la respuesta esté en formato de texto plano y contenga únicamente la palabra, 
frase o letras que completan el texto. El formato que debe tener la respuesta es un JSON 
devolviendo {"status": "success", "text": "completion text"} si la frase se puede completar, y 
{"status": "error", "message": "include why you can't complete"} si no se puede completar.

Ejemplo de Uso:

Ejemplo 1:
Frase a completar: "Hel"  
Respuesta esperada: {"status": "completed", "text": "Hola"}

Ejemplo 2:
Frase a completar: "Hi, my name is"  
Respuesta esperada: {"status": "completed", "text": "Matias."}

Ejemplo 3:
Frase a completar: "Buy some"  
Respuesta esperada: {"status": "completed", "text": "milk"}

De esta forma, la IA debería devolverte únicamente la palabra, frase o letras que completan el texto, 
sin explicaciones adicionales y con el formato JSON esperado. Necesito que en caso de no poder 
completar cumplas con el JSON y su estado correspondiente, agregando un mensaje en la casilla "text" 
del porqué no pudiste completar.
"""


def get_autocomplete_agent_prompt(title: str, list_tasks: list, petition: str):
    list_tasks_str = json.dumps(list_tasks, ensure_ascii=False)
    prompt = (
        autocomplete_agent.replace("title", title)
        .replace("list_tasks", list_tasks_str)
        .replace("petition", petition)
    )
    return prompt
