
# coding: utf-8

# # Trabajo final data mining

# En este trabajo brindaremos un chat bot de respuestas cortas para IM en español. Primero que nada definiremos una respuesta corta como cualquier turno hasta 3 palabras que ocurren al menos n veces. Iremos probando diferentes n a modo de prueba. El texto anterior a la respuesta corta será llamado contexto

# ## Extracción del corpus

# Debido a que no hay un corpus bien definido para este problema utilizaremos el contexto del chat como texto de entrenamiento, por lo que la respuesta corta será la etiqueta.

# ### Procesamiento

# In[75]:


import re
import csv
from datetime import datetime, timedelta


# #### Conociendo los datos "crudos"

# In[52]:


with open('whatsapp/chat1.txt') as f:
    raw_data = f.readlines()
print(raw_data)


# Sacaremos la primera línea que de nada sirve
# 
# `6/18/17, 16:43 - Los mensajes y llamadas en este chat ahora están protegidos con cifrado de extremo a extremo. Toca para más información.`

# #### Tratando de preprocesar
# 
# Para ello spliteo cada línea por la primera ocurrencia de ": ". Meteremos todo en un mismo contexto si la misma persona escribe durante una hora y media. Ver bien si se puede hacer algo con las líneas que no tengan el mismo formato.

# In[85]:


info_chat = []

for line in raw_data:
    if "-" not in line or ": " not in line:
        continue
    info, text = line.split(": ", 1)
    if '<Archivo omitido>' in text:
        continue
    date, owner = info.split(" - ", 1)
    date, hour = date.split(", ")
    hours, mins = hour.split(":")
    month, day, year = date.split("/")
    info_chat.append([owner, datetime(int(year), int(month), int(day), int(hours), int(mins)), text.split('\n')[0]])
info_chat


# Ahora agruparemos los contextos con sus respectivas respuestas. Guardaremos el corpus en formato CSV.

# In[79]:


HOUR = 60
SAME_CONTEXT = timedelta(seconds=24*HOUR)

SHORT_ANSWER = 3
def is_short(answer):
    """
    is short answer?
    """
    return len(answer.split(' ')) <= SHORT_ANSWER

def is_same_context(hour1, hour2):
    """
    hour1 must be larger-equal than hour2
    """
    return hour1 - hour2 <= SAME_CONTEXT


# In[86]:


corpus_data = []

with open('corpus.csv', 'w', newline='') as csvfile:
    fieldnames = ['context', 'label']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    last_owner = ''
    row = {'context':'', 'label':''}
    for i, (owner, time, text) in enumerate(info_chat):
        if owner != last_owner:
            if is_short(text):
                row['label'] = text
                writer.writerow(row)
                row = {'context':text, 'label':''}
            else:
                row['context'] += ' ' + text
        else:
            if is_short(text):
                row['label'] = text
                writer.writerow(row)
            row['context'] += ' ' + text

        last_owner = owner
                

