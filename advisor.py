'''Grounded training-advice generator using a rented chat model.

The model is instructed to use only retrieved notes. If the evidence is not
sufficient, it must abstain. This makes unsupported invention directly testable.
'''
import os, json, getpass
from openai import OpenAI

MODEL='openai/gpt-4o-mini'
SYSTEM='''You are a beginner badminton training assistant.
Use ONLY the supplied NOTES. Do not add facts, timings, repetitions, diagnoses,
or safety claims that are not present in the notes.
Return concise JSON with keys: category, likely_issue, drill, evidence_note_ids.
The drill must be specific and actionable. If the notes do not support a useful
answer, set likely_issue and drill to "The notes do not say" and use an empty
evidence_note_ids list.'''

def get_key(explicit_key=None):
    if explicit_key:
        return explicit_key.strip()
    key=os.environ.get('MY_PRIVATE_OPENROUTER_KEY') or os.environ.get('OPENROUTER_API_KEY')
    if key:
        return key.strip()
    try:
        from google.colab import userdata
        key=userdata.get('MY_PRIVATE_OPENROUTER_KEY')
        if key:
            return key.strip()
    except Exception:
        pass
    return getpass.getpass('OpenRouter API key (hidden): ').strip()

def client(api_key=None):
    return OpenAI(base_url='https://openrouter.ai/api/v1', api_key=get_key(api_key))

def advise(question, category, hits, model=MODEL, api_key=None):
    notes='\n'.join(f"[{h['id']}] {h['text']}" for h in hits)
    prompt=f"USER QUESTION: {question}\nROUTED CATEGORY: {category}\n\nNOTES:\n{notes}"
    response=client(api_key).chat.completions.create(
        model=model,
        messages=[{'role':'system','content':SYSTEM},{'role':'user','content':prompt}],
        temperature=0,
        max_tokens=220,
    )
    text=response.choices[0].message.content.strip()
    if text.startswith('```'):
        text=text.strip('`')
        if text.lower().startswith('json'):
            text=text[4:].strip()
    obj=json.loads(text)
    usage=getattr(response,'usage',None)
    meta={
        'prompt_tokens': getattr(usage,'prompt_tokens',None) if usage else None,
        'completion_tokens': getattr(usage,'completion_tokens',None) if usage else None,
        'model': model,
    }
    return obj,meta
