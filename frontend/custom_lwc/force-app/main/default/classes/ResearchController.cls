public with sharing class ResearchController {
    @AuraEnabled(cacheable=false)
    public static String fetchTicker(String ticker) {
        Http http = new Http();
        HttpRequest req = new HttpRequest();

        req.setEndpoint('https://nw-s25.onrender.com/research/' + EncodingUtil.urlEncode(ticker, 'UTF-8'));
        req.setMethod('GET');

        HttpResponse res = http.send(req);
        return res.getBody(); // returns raw JSON string
    }
}


