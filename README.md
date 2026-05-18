# secure-web-toolkit

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Flask](https://img.shields.io/badge/Flask-Latest-green) ![License](https://img.shields.io/badge/License-MIT-yellow) ![OWASP](https://img.shields.io/badge/OWASP-ZAP-red) ![RAG](https://img.shields.io/badge/RAG-FAISS%20%2B%20Ollama-purple)

A Flask-based web application combining three powerful cybersecurity tools: **AES+RSA file encryption**, **OWASP ZAP vulnerability scanning**, and a **RAG-powered security chatbot** backed by FAISS and Ollama.

---

## Features

- **File Encryption** — Encrypt and decrypt any file using AES-256-GCM + RSA-2048 key encapsulation with HMAC integrity verification
- - **Vulnerability Scanner** — Scan any website for security vulnerabilities using OWASP ZAP (Fast & Full scan modes)
  - - **Security Chatbot** — Ask cybersecurity questions and get answers powered by a local RAG pipeline (FAISS + Ollama phi3)
    - - **Audit Logging** — All encryption/decryption operations are logged for accountability
     
      - ---

      ## Project Structure

      ```
      secure-web-toolkit/
      └── IS-UPDATED_PROJECT/
          └── project_root/
              └── backend/
                  ├── app.py                  # Flask app & API routes
                  ├── requirements.txt        # Python dependencies
                  ├── file_security.log       # Encryption audit log
                  ├── services/
                  │   ├── crypto.py           # AES+RSA encryption/decryption
                  │   ├── zap_scanner.py      # OWASP ZAP scanner wrapper
                  │   ├── scan_manager.py     # Async scan job manager
                  │   └── chatbot.py          # RAG chatbot (FAISS + Ollama)
                  ├── templates/
                  │   ├── index.html          # Home page
                  │   ├── encrypt.html        # Encryption UI
                  │   ├── scanner.html        # Scanner UI
                  │   └── chatbot.html        # Chatbot UI
                  ├── data/                   # Cybersecurity knowledge base
                  │   ├── NIST_guidelines.txt
                  │   ├── OWASP_Top10.txt
                  │   ├── XSS.txt
                  │   ├── phishing.txt
                  │   └── ransomware.txt
                  ├── faiss_index/            # Pre-built vector index
                  │   ├── index.faiss
                  │   └── metadata.pkl
                  ├── keys/                   # RSA key pair
                  │   ├── private.pem
                  │   └── public.pem
                  └── uploads/               # Temporary file storage
      ```

      ---

      ## Prerequisites

      - Python 3.10+
      - - [OWASP ZAP](https://www.zaproxy.org/download/) installed and running on `localhost:8080`
        - - [Ollama](https://ollama.com/) installed with the `phi3` model pulled
         
          - ```bash
            ollama pull phi3
            ```

            ---

            ## Installation & Setup

            ### 1. Clone the repository
            ```bash
            git clone https://github.com/zohacust-debug/secure-web-toolkit.git
            cd secure-web-toolkit/IS-UPDATED_PROJECT/project_root/project_root/backend
            ```

            ### 2. Create a virtual environment
            ```bash
            python -m venv venv
            venv\Scripts\activate        # Windows
            # source venv/bin/activate   # Mac/Linux
            ```

            ### 3. Install dependencies
            ```bash
            pip install -r requirements.txt
            ```

            ### 4. Start OWASP ZAP
            Launch ZAP and make sure it's listening on `http://127.0.0.1:8080`

            ### 5. Start Ollama
            ```bash
            ollama serve
            ```

            ### 6. Run the Flask app
            ```bash
            python app.py
            ```

            Open your browser and go to: `http://127.0.0.1:5000`

            ---

            ## Usage

            ### File Encryption
            - Go to `/encrypt`
            - - Upload any file (PDF, DOCX, image, ZIP, etc.)
              - - Download the `.enc` encrypted file
                - - Upload the `.enc` file again to decrypt it back
                 
                  - ### Vulnerability Scanner
                  - - Go to `/scanner`
                    - - Enter a target URL (must be a site you own or have permission to scan)
                      - - Choose **Fast** (spider + passive) or **Full** (spider + passive + active) scan
                        - - View detected vulnerabilities with severity ratings
                         
                          - ### Security Chatbot
                          - - Go to `/chatbot`
                            - - Ask questions about OWASP Top 10, XSS, phishing, ransomware, NIST guidelines
                              - - Get contextual answers powered by local LLM (no internet needed)
                               
                                - ---

                                ## Tech Stack

                                | Component | Technology |
                                |-----------|-----------|
                                | Backend | Python, Flask |
                                | Encryption | AES-256-GCM, RSA-2048, HMAC |
                                | Vulnerability Scanning | OWASP ZAP (python-owasp-zap-v2.4) |
                                | RAG Pipeline | FAISS, Sentence Transformers, Ollama (phi3) |
                                | Frontend | HTML, CSS, JavaScript |

                                ---

                                ## Requirements

                                ```
                                flask
                                cryptography
                                python-owasp-zap-v2.4
                                faiss-cpu
                                sentence-transformers
                                requests
                                numpy
                                ollama
                                ```

                                ---

                                ## Important Notes

                                > The vulnerability scanner is intended for use on websites you **own or have explicit permission to test**. Unauthorized scanning of systems is illegal and unethical.
                                >
                                > > RSA keys are auto-generated on first run and stored in the `keys/` folder. Keep your `private.pem` safe.
                                > >
                                > > ---
                                > >
                                > > ## License
                                > >
                                > > This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
                                > >
                                > > ---
                                > >
                                > > ## Author
                                > >
                                > > **zohacust-debug** — [GitHub Profile](https://github.com/zohacust-debug)
