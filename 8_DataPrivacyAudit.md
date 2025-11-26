# Data Privacy Audit – WhatsApp

## 1. Overview of WhatsApp and Data Flows

WhatsApp is a global messaging application owned by Meta. It offers:

- One-to-one and group text messaging  
- Voice and video calls  
- Media/file sharing  
- Status updates  
- Business messaging features  

Most users assume that because chats are end-to-end encrypted, WhatsApp cannot access their data. This is true for **message content**, but the app still processes a lot of **metadata** (who you talk to, when, from which device, etc.) and depends on cloud providers for backups and device operating systems for security.

---

## 2. Encryption and Decryption Processes

### 2.1 End-to-End Encryption for Messages

WhatsApp uses the **Signal Protocol** for end-to-end encryption (E2EE). In simple terms:

1. **Key Generation (on device)**
   - Each user’s device creates:
     - A long-term **identity key pair** (public + private).
     - Additional **ephemeral keys** used for sessions.
   - Public keys are sent to WhatsApp’s server; **private keys never leave the device**.

2. **Session Setup (when you start a chat)**
   - When User A first messages User B, A’s app requests B’s public keys from the server.
   - Using a key agreement method (based on Curve25519, X3DH, and the Double Ratchet concept), both devices derive a **shared secret**.
   - This secret is then turned into **symmetric encryption keys** for messages.

3. **Message Encryption (on sender’s device)**
   - For each message:
     - A fresh, per-message **session key** is generated using the Double Ratchet algorithm.
     - The message body (text, attachments) is encrypted with a symmetric cipher (e.g., AES-256 in an authenticated mode).
     - A message authentication code (MAC) or AEAD tag ensures integrity (message can’t be silently modified).

4. **Transport (via WhatsApp servers)**
   - Encrypted messages travel through WhatsApp’s servers.
   - Servers can see **routing info** (sender, receiver, timestamps, delivery state), but **not the clear text**.

5. **Decryption (on receiver’s device)**
   - Receiver’s device uses its private keys plus the ratchet state to derive the correct session key.
   - It decrypts the ciphertext locally.
   - If keys don’t match (e.g., new phone), users can verify security codes.

6. **Group Chats**
   - Each group member has their own pairwise encrypted channel.
   - A sender encrypts a message separately for each recipient (or uses a group key derived via Signal-style protocol), so only group members can read it.

### 2.2 Encryption of Backups

WhatsApp supports **cloud backups** to Google Drive (Android) and iCloud (iOS).

- Historically, backups were **not end-to-end encrypted** and could be accessed by cloud providers or law enforcement with legal orders.
- Since 2021, WhatsApp offers **optional end-to-end encrypted backups**:
  - User chooses a **password or a 64-digit encryption key**.
  - Backup is encrypted on the device before upload.
  - Neither WhatsApp nor Google/iCloud can decrypt it if this option is enabled.
- In 2025, WhatsApp started adding **passkey-based protection** to make backup encryption easier to use (face/fingerprint/phone PIN instead of remembering a long key).

Risk: Many users may **not enable** E2EE backups, so their chat history in the cloud can still be accessed if their cloud account is compromised or served under legal orders.

---

## 3. Data Collected and Metadata

Even with E2EE, WhatsApp collects and/or processes:

- **Account data**
  - Phone number
  - Profile photo, “About” text, status
  - Device information (model, OS, app version)
- **Usage metadata**
  - Who you talk to (contact list hashes / phone numbers)
  - When you send/receive messages (timestamps)
  - Group memberships
  - Approximate location via IP address and country/region info
- **Diagnostics & analytics**
  - Crash logs
  - Performance metrics
- **Data sharing with Meta**
  - Certain metadata may be shared with other Meta services for security, spam prevention, and (outside some regions) **advertising and product improvement**.

Important: **Message content** (chats, calls, media) is encrypted and not visible to WhatsApp or Meta when E2EE works correctly. However, **metadata is not encrypted end-to-end** and can be used for profiling, targeted ads (through Meta ecosystem), and law-enforcement or other requests.

---

## 4. Identified Vulnerabilities and Risks

### 4.1 Metadata Exposure and Data Sharing

- WhatsApp’s privacy policy allows collection of rich metadata (who talks to whom, how often, on which device, etc.).
- Changes in 2016 and 2021 increased data sharing with Facebook/Meta in many regions.
- Even without reading messages, this metadata can reveal:
  - Social graph (your network)
  - Activity patterns (online at night, travel times)
  - Possible interests or affiliations (e.g., groups joined, business accounts contacted).

**Risk:** Users may believe “end-to-end encrypted” means “no data is collected,” which is not true. Metadata remains a significant privacy risk.

---

### 4.2 Contact Discovery and Phone Number Exposure

Recent academic research found a serious issue in WhatsApp’s **contact discovery mechanism**:

- By sending huge volumes of phone numbers for “contact sync,” researchers could:
  - Confirm which numbers are on WhatsApp (up to ~100 million numbers per hour).
  - Collect metadata such as device type, profile photo, account age, and sometimes approximate location.
- This affected almost all ~3.5 billion WhatsApp accounts before Meta patched it.

**Cause:**  
The contact discovery API allowed high-volume queries without sufficient rate limiting or anonymization. It effectively enabled **mass scraping** of WhatsApp user metadata.

**Risk:**  
Attackers can build massive databases of active WhatsApp numbers for:

- Targeted phishing and scams  
- Harassment  
- Intelligence and profiling on a population scale  

---

### 4.3 Large-Scale Phone Number Scraping (“500M Numbers Leak”)

In 2022, a dataset containing **hundreds of millions of WhatsApp phone numbers** was advertised for sale on hacker forums. Investigations indicated:

- Numbers were likely collected using **automated scraping**, not by breaking encryption.
- The data included the fact that the number uses WhatsApp, country information, and sometimes additional metadata.

**Cause:**  
Abuse of public-facing interfaces (such as WhatsApp’s registration / contact discovery) and poor rate limiting, allowing an attacker to test or enumerate large ranges of phone numbers.

**Risk:**  
Even without message content, a list of active numbers can be used for:

- Spam and scam campaigns  
- SIM-swap / social engineering attacks  
- Correlation with other breached databases

---

### 4.4 Group Invite Links Indexed on Search Engines

Several times, **WhatsApp group invite links** have been **indexed by Google** and other search engines:

- Users or admins shared invite links on public websites or social media.
- Search engines crawled these pages, making private groups discoverable via simple searches.
- Anyone could click the link and **join the group**, seeing phone numbers and messages from that point onward.

**Causes:**

- Design choice: Group invites are simple URLs that behave like open-door tokens.
- Users shared links in public spaces.
- Initially missing or inconsistent use of `noindex` tags on invite pages.

**Risks:**

- Exposure of members’ phone numbers and group names.
- Sensitive groups (e.g., workplace, school, activist or health support groups) unintentionally became semi-public.

Mitigation steps have been taken (adding `noindex`, advising users), but the risk depends heavily on user behavior and search engine respect for indexing hints.

---

### 4.5 Device Compromise and Pegasus Spyware

In 2019, the **NSO Group’s Pegasus spyware** exploited a vulnerability in WhatsApp’s call handling:

- A specially crafted **missed WhatsApp call** could silently install Pegasus on the device.
- Once installed, Pegasus had deep OS-level access:
  - Microphone, camera, messages (before/after encryption), emails, location, etc.
- Around a thousand+ users worldwide (journalists, activists, diplomats) were targeted.

WhatsApp/Meta later sued NSO and, in 2024–2025, won a significant damages award in court.

**Cause:**

- A memory / logic bug in WhatsApp’s VoIP stack allowed **remote code execution**.
- Attackers exploited this to bypass application-level encryption by controlling the device itself.

**Risk:**

- E2EE cannot protect against **device-level compromise**.
- If malware controls your phone, it can read messages **before encryption** or **after decryption**.

---

### 4.6 Backup and Account Compromise

Even with E2EE backups:

- If a user does **not** enable encrypted backups:
  - Chat contents in Google Drive or iCloud can be accessed by anyone who gains access to those accounts or by authorities via cloud providers.
- If a user **does** enable encrypted backups:
  - Security depends on:
    - Strength of the backup password / key.
    - Protection of the device and password (or new passkey mechanism).
- Research has also shown that if an attacker can access a user’s encrypted backup and can inject chosen data (via messages), they may infer some information from ciphertext lengths.

**Risks:**

- Compromise of cloud account (e.g., weak password, phishing).
- Loss or sharing of backup encryption password/key.
- Side-channel analysis in advanced threat models.

---

## 5. Summary of Key Incidents (Attacks / Leaks)

| Year (approx.) | Incident / Issue                                      | Data Affected                                | Root Cause                                                                                   |
|----------------|--------------------------------------------------------|----------------------------------------------|----------------------------------------------------------------------------------------------|
| 2019           | Pegasus spyware via WhatsApp missed-call vulnerability | Targeted users’ full device data & chats     | Memory / logic bug in VoIP call handling, enabling remote code execution on devices          |
| 2020–2021      | Group invite links indexed by Google                  | Group membership, phone numbers, group names | Public sharing of invite links + search engine indexing; insufficient `noindex` early on     |
| 2021           | Controversial privacy policy update                   | Expansion of metadata sharing with Meta       | Policy change to allow broader data sharing for analytics/ads in many regions               |
| 2021–2022      | Phone numbers of ~500M users advertised for sale      | Phone numbers, country info, WhatsApp usage  | Bulk scraping through contact discovery / enumeration; limited rate limiting                 |
| 2024–2025      | Contact discovery flaw (3.5B accounts exposed)        | Phone numbers, device type, account age, etc | Contact discovery API allowed high-volume lookups without adequate rate limiting or privacy  |

---

## 6. Overall Privacy Risk Rating

- **Message content security:**  
  - **Strong**, when E2EE and verified keys are used and the device is not compromised.
- **Metadata privacy:**  
  - **Moderate to weak**, due to extensive metadata collection and sharing with Meta plus susceptibility to scraping and legal requests.
- **User behavior and configuration risk:**  
  - **Moderate**, especially if users:
    - Don’t enable encrypted backups,
    - Share group invite links publicly,
    - Use weak device or cloud security.

---

## 7. Recommendations

### 7.1 For WhatsApp / Meta

1. **Harden contact discovery**
   - Strong rate limiting, anomaly detection, and privacy-preserving contact discovery (e.g., private set intersection) to reduce scraping.
2. **Minimize metadata**
   - Collect only what is strictly necessary; shorten retention periods.
   - Provide clearer, more granular opt-outs for data sharing with other Meta services.
3. **Default E2EE backups**
   - Make encrypted backups **opt-out instead of opt-in** and improve backup key recovery UX.
4. **Stronger group invite controls**
   - Default invite links to short expiry.
   - Clear warnings before users post invites publicly.
5. **Improved transparency**
   - Regular, detailed transparency reports about law-enforcement requests, scraping incidents, and major vulnerabilities.
6. **Secure development**
   - Continue rigorous security testing (fuzzing, bug bounties) for media handling and VoIP components to avoid Pegasus-style exploits.

### 7.2 For Users

1. **Enable end-to-end encrypted backups** and protect them with a strong password or passkey.
2. **Avoid sharing group invite links** on public websites or social media.
3. **Keep your phone OS and WhatsApp updated** to get latest security patches.
4. **Use strong screen locks** and secure your Google/iCloud accounts with strong passwords and multi-factor authentication.
5. **Be skeptical of unknown calls and messages**, especially links and attachments from strangers.
6. **Review privacy settings** inside WhatsApp:
   - Who can see your profile photo, about, status, last seen, and online status.
   - Whether to share data with Meta services where options exist.

---

## 8. Audit Conclusion

WhatsApp provides **industry-leading message content protection** via the Signal Protocol and now extends that protection to backups (if enabled). However, significant **privacy risks** remain around:

- Metadata collection and sharing within the Meta ecosystem.  
- Large-scale scraping and enumeration of phone numbers and profile data.  
- Device-level attacks (e.g., spyware) that bypass app-level encryption.  

For high-risk users (journalists, activists, vulnerable groups), careful configuration of security settings, secure backups, hardened devices, and cautious sharing of contact/group details are essential. For ordinary users, WhatsApp is generally secure against casual interception of message content, but they should understand that **“encrypted messages” does not equal “no data collected.”**

