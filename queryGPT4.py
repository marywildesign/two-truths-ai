import time
import json
import numpy as np
import openai as oai
import os
import textwrap

key = open('../.key.txt','r').readlines()[0]
oai.api_key = key

if not os.path.isdir('./gpt-outputs/'):
    os.mkdir('./gpt-outputs/')

def create_prompt(subject):
    return (f'Provide me with two truths and one lie about {subject}. '
            'Always put the lie last.'
            'Never point out the lie in what you write.'
            'Make the lie challenging to identify.'
            'Do not use an easily spotted lie.'
            'Make the lie a funny joke if you see a good possibility to.'
            'Remove any empty lines from your reply.'
            'Place each statement on its own line.'
            'Do not put any empty lines in your response, especially not following periods'
            'Do not use hyphens, bullets, asterisks, line breaks, or numbers to indicate the sequence or order of your three statements.'
            'Make each reply contain exactly two line breaks.'
            )

subjects = ['oslo art',
            'graphic design',
            'typography',
            'brutalism design',
            'fluxus design',
            'bauhaus design',
            'australia fun facts',
            'colour theory',
            'art theory',
            'minimalist design',
            'swiss design',
            'architecture styles',
            'fashion movements'
           ]

NperPrompt = 40  # number of outputs per prompt

data = []
idx = 0
for subject in subjects:
    prompt = create_prompt(subject)
    for n in range(NperPrompt):  # generate NperPrompt distinct outputs per prompt
        response = oai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            seed=n
        )
        output = response.choices[0].message.content.strip()
        time.sleep(0.5) # reduced sleep time
        
        # now you have the output from the model, output. This contains truths and lies separated by line breaks \n and possibly \n\n empty lines.        
        # if there are any double line breaks (i.e., an empty line \n\n) in the output, replace with a single line break.
        output = output.replace('\n\n', '\n')
        # check now that there are exactly three entries upon splitting on the line breaks, two truths and one lie in the chatgpt output
        entries = output.split('\n')
        if len(entries)==3:
            tru1, tru2, lie = entries # unpack the entries
            if (len(tru1)==0) | (len(tru2)==0) | (len(lie)==0):
                print('Warning! An entry has zero length in the json file and field %d requires deletion.'%idx)
            # now write one new entry to the json file
            item = {'id':idx,
                    'truth1':tru1,
                    'truth2':tru2,
                    'lie':lie
                    }
            # now record an entry for future saving
            data.append(item)
            print('Entry %d recorded.'%(idx+1))
            idx+=1 # increase the count by 1.
        else:
            print('gpt failed to produce properly formatted output. Skipping to the next call to the model.')
        print('---------------------------------------')

print('Chatgpt query complete. Saving data to JSON.')
# Writing to a JSON file
with open('data.json', 'w') as json_file:
#with open('../data/website/data.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)  # indent for pretty printing
print('Saving complete.')
