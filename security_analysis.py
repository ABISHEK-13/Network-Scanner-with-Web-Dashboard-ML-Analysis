from sklearn.ensemble import IsolationForest
import numpy as np

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)

        normal_data = np.array([
            [22, 10], [80, 15], [443, 12], [53, 8],
            [110, 20], [25, 18], [143, 16], [993, 14]
        ])
        self.model.fit(normal_data)

    def extract_features(self, scan_results):
        features = []
        ports = []
        for entry in scan_results:
            if entry['status'] == 'open':
                port = entry['port']
                banner = entry.get('banner', '')
                ports.append(port)
                features.append([port, len(banner)])
        return np.array(features), ports

    def detect(self, scan_results):
        features, ports = self.extract_features(scan_results)
        if len(features) == 0:
            return []

        preds = self.model.predict(features)
        scores = self.model.decision_function(features)

        anomalies = []
        for i in range(len(preds)):
            if preds[i] == -1:
                anomalies.append({
                    'port': ports[i],
                    'risk_score': -scores[i]
                })
        return anomalies

