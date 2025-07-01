public with sharing class RecommendationController {
    @AuraEnabled
    public static String getRecommendation(String sector, String marketCapLevel, String growthValueType, String forwardPE) {
        Http http = new Http();
        HttpRequest req = new HttpRequest();

        Map<String, Object> body = new Map<String, Object>{
            'sector' => sector,
            'marketCapLevel' => marketCapLevel,
            'growthValueType' => growthValueType,
            'forwardPE' => forwardPE
        };
        String jsonBody = JSON.serialize(body);

        req.setEndpoint('https://nw-s25.onrender.com/research/recommendations'); 
        req.setMethod('POST');
        req.setHeader('Content-Type', 'application/json');
        req.setBody(jsonBody);

        HttpResponse res = http.send(req);
        return res.getBody();  // response.body = { "message": "{\"recs\": [\"AAPL\", \"MSFT\"]}" }
    }
}
