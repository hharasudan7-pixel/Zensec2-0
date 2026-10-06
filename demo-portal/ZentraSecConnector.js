class ZentraSecConnector {
  constructor(apiUrl, connectionId, secureToken) {
    this.apiUrl = apiUrl;
    this.connectionId = connectionId;
    this.secureToken = secureToken;
    this.userId = null;
  }

  setUserId(userId) {
    this.userId = userId;
  }

  async sendEvent(eventType, metadata = {}) {
    const payload = {
      connection_id: this.connectionId,
      timestamp: new Date().toISOString(),
      user_id: this.userId || "anonymous",
      source_ip: "", // Let backend extract this via request.client.host
      destination: "demo-portal",
      event_type: eventType,
      metadata: metadata // Pass as object, backend expects Dict
    };

    try {
      console.log(`[ZentraSec] ${eventType} event generated`);
      console.log(`[ZentraSec] Sending event to ${this.apiUrl}/api/v1/events`);
      const response = await fetch(`${this.apiUrl}/api/v1/events`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${this.secureToken}`
        },
        body: JSON.stringify(payload)
      });
      console.log(`[ZentraSec] Response status: ${response.status}`);
      if (!response.ok) {
        console.error(`[ZentraSec] Failed to send telemetry! HTTP ${response.status}`);
        alert("Failed to send telemetry! HTTP " + response.status);
      }
      return await response.json();
    } catch (e) {
      console.error("ZentraSec Telemetry Error:", e);
      alert("Telemetry Error: " + e.message);
    }
  }

  async login(username, success, method = "password") {
    this.setUserId(username);
    return this.sendEvent(success ? "LOGIN_SUCCESS" : "LOGIN_FAILURE", { method });
  }

  async logout() {
    return this.sendEvent("LOGOUT");
  }

  async updateProfile() {
    return this.sendEvent("PROFILE_UPDATE");
  }

  async accessAdminPanel() {
    return this.sendEvent("PRIVILEGE_ACCESS", { resource: "/admin" });
  }

  async downloadLargeFile(filename) {
    return this.sendEvent("LARGE_FILE_DOWNLOAD", { file: filename });
  }

  async register(username) {
    return this.sendEvent("USER_REGISTRATION", { username });
  }

  async resetPassword(username) {
    return this.sendEvent("PASSWORD_RESET_REQUEST", { username });
  }
}
