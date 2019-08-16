from vibora import Vibora, Request
from vibora.responses import JsonResponse
from spacypiidetector.piidetector import PiiDetector
import json

app = Vibora()

@app.route('/spacy_ner',methods=['POST'])
async def spacy_ner(request: Request):
        json = await request.json()
        print(json["text"])
        entities = PiiDetector().getEntites(json['text'])
        return JsonResponse(entities)

@app.route('/spacy_regex',methods=['POST'])
async def spacy_ner(request: Request):
        json = await request.json()
        print(json["text"])
        entities = PiiDetector().getpatterns(json['text'])
        return JsonResponse(entities)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)