import org.apache.http.HttpEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

// Add your Azure Ink Recognition subscription key to your environment variables.
private static final String subscriptionKey = System.getenv("INK_RECOGNITION_SUBSCRIPTION_KEY");

// Add your Azure Ink Recognition endpoint to your environment variables.
public static final String rootUrl = System.getenv("INK_RECOGNITION_ENDPOINT");
public static final String inkRecognitionUrl = "/inkrecognizer/v1.0-preview/recognize";
// Replace the dataPath string with a path to the JSON formatted ink stroke data file.
private static final String dataPath = "/home/nina/autograder/INKdata/TrainINKML_2013";


static String sendRequest(String endpoint, String apiAddress, String subscriptionKey, String requestData) {
    try (CloseableHttpClient client = HttpClients.createDefault()) {
        HttpPut request = new HttpPut(endpoint + apiAddress);
        // Request headers.
        request.setHeader("Content-Type", "application/json");
        request.setHeader("Ocp-Apim-Subscription-Key", subscriptionKey);
        request.setEntity(new StringEntity(requestData));
        try (CloseableHttpResponse response = client.execute(request)) {
            HttpEntity respEntity = response.getEntity();
            if (respEntity != null) {
                return EntityUtils.toString(respEntity, "utf-8");
            }
        } catch (Exception respEx) {
            respEx.printStackTrace();
        }
    } catch (IOException ex) {
        System.err.println("Exception on Anomaly Detector: " + ex.getMessage());
        ex.printStackTrace();
    }
    return null;
}


static void recognizeInk(String requestData) {
    System.out.println("Sending an Ink recognition request.");

    String result = sendRequest(rootUrl, inkRecognitionUrl, subscriptionKey, requestData);
    System.out.println(result);
}


public static void main(String[] args) throws Exception {

    String requestData = new String(Files.readAllBytes(Paths.get(dataPath)), "utf-8");
    recognizeInk(requestData);
}
