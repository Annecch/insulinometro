#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <BLECharacteristic.h>

// UUID del servizio e della caratteristica
#define SERVICE_UUID           "12345678-1234-5678-1234-56789abcdef0"
#define CHARACTERISTIC_UUID    "12345678-1234-5678-1234-56789abcdef1"

// Variabili per la caratteristica
BLECharacteristic *pCharacteristic;

// Funzione per generare una temperatura casuale tra 20 e 30 gradi Celsius
float generateRandomTemperature() {
  return 20 + (rand() % 1000) / 100.0;  // Valore tra 20.00 e 29.99
}

// Callback per la scrittura sulla caratteristica
class MyCharacteristicCallbacks : public BLECharacteristicCallbacks {
  void onWrite(BLECharacteristic *pCharacteristic) {
    // Quando viene scritto un dato nella caratteristica
    String value = pCharacteristic->getValue().c_str();  // Usa String invece di std::string
    Serial.print("Dati ricevuti: ");
    Serial.println(value);
    
    // Rispondere al client con un messaggio
    pCharacteristic->setValue("Dati ricevuti correttamente");
    pCharacteristic->notify();  // Notifica al client che i dati sono stati ricevuti
  }
};

void setup() {
  // Inizializza la comunicazione seriale, Configura la porta seriale per il debug con un baud rate di 115200.
  Serial.begin(115200);
  
  // Inizializza il BLE
  BLEDevice::init("ESP32_BLE_Server_Gruppo_H");
  
  // Crea un server BLE
  BLEServer *pServer = BLEDevice::createServer();
  
  // Crea il servizio BLE
  BLEService *pService = pServer->createService(SERVICE_UUID);
  
  // Crea una caratteristica per il servizio (scrivibile e leggibile)
  pCharacteristic = pService->createCharacteristic(
                      CHARACTERISTIC_UUID,
                      BLECharacteristic::PROPERTY_READ |
                      BLECharacteristic::PROPERTY_WRITE |
                      BLECharacteristic::PROPERTY_NOTIFY
                    );
  
  // Imposta il callback per la scrittura sulla caratteristica
  pCharacteristic->setCallbacks(new MyCharacteristicCallbacks());
  
  // Avvia il servizio
  pService->start();
  
  // Avvia la pubblicità BLE per rendere il dispositivo visibile
  BLEAdvertising *pAdvertising = pServer->getAdvertising();
  pAdvertising->start();
  
  Serial.println("Server BLE avviato, in attesa di connessione...");
}

void loop() {
  // Genera una temperatura casuale
  float temperature = generateRandomTemperature();
  
  // Converte il valore in stringa e aggiorna la caratteristica
  String tempStr = String(temperature, 2);  // Limita a 2 decimali
  pCharacteristic->setValue(tempStr.c_str());
  
  // Invia una notifica (opzionale, per far sapere al client che il valore è cambiato)
  pCharacteristic->notify();
  
  // Stampa il valore sulla seriale per il debug
  Serial.print("Temperatura generata: ");
  Serial.println(tempStr);
  
  // Fai una pausa di 5 secondi
  delay(5000);
}
