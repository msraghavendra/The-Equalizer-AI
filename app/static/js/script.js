function openTab(tabId) {
    // Hide all contents
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });

    // Deactivate all buttons and find the one that targets this tab
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        // Check if the button's onclick attribute targets this tabId
        const onclickAttr = btn.getAttribute('onclick') || '';
        if (onclickAttr.includes(`'${tabId}'`)) {
            btn.classList.add('active');
        }
    });

    // Show selected content
    const target = document.getElementById(tabId);
    if (target) {
        target.classList.add('active');
    }
}

// New File Upload Logic
async function uploadFile(url, fileInputId, resultBoxId) {
    const fileInput = document.getElementById(fileInputId);
    if (!fileInput.files[0]) {
        alert("Please select a file first!");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    setLoading(true);
    const resultBox = document.getElementById(resultBoxId);

    try {
        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        setLoading(false);
        resultBox.classList.remove('hidden');
        resultBox.innerHTML = formatOutput(result.analysis);
    } catch (error) {
        setLoading(false);
        resultBox.classList.remove('hidden');
        resultBox.innerHTML = "Error: Could not upload or process file.";
    }
}

async function analyzeFile() {
    await uploadFile('/analyze/file', 'analyze-file', 'analyze-result');
}

async function simplifyFile() {
    await uploadFile('/simplify/file', 'simplify-file', 'simplify-result');
}

// API Helper
async function postData(url = '', data = {}) {
    setLoading(true);
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        setLoading(false);
        return result;
    } catch (error) {
        setLoading(false);
        return { analysis: "Error: Could not connect to the server." };
    }
}

function setLoading(isLoading) {
    const btns = document.querySelectorAll('.action-btn');
    const resultBoxes = document.querySelectorAll('.result-box');

    btns.forEach(btn => {
        if (isLoading) {
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
            btn.disabled = true;
            // Add scanning class to the relevant result box if it exists
            const tabContent = btn.closest('.tab-content');
            const resultBox = tabContent ? tabContent.querySelector('.result-box') : null;
            if (resultBox) {
                resultBox.classList.remove('hidden');
                resultBox.classList.add('scanning');
                resultBox.innerHTML = '<p style="text-align: center; color: var(--text-muted);">Scanning document for risks...</p>';
            }
        } else {
            btn.innerHTML = 'Analysis Complete';
            btn.disabled = false;
            // Remove scanning class
            resultBoxes.forEach(box => box.classList.remove('scanning'));

            setTimeout(() => {
                const onclickStr = btn.getAttribute('onclick') || '';
                if (onclickStr.includes('analyzeDocument')) btn.innerHTML = 'Analyze Risks';
                else if (onclickStr.includes('simplifyDocument')) btn.innerHTML = 'Simplify Text';
                else if (onclickStr.includes('analyzeFile')) btn.innerHTML = '<i class="fa-solid fa-file-upload"></i> Analyze Uploaded File';
                else if (onclickStr.includes('simplifyFile')) btn.innerHTML = '<i class="fa-solid fa-file-upload"></i> Simplify Uploaded File';
                else if (onclickStr.includes('translate')) btn.innerHTML = 'Translate & Speak';
                else if (onclickStr.includes('generate')) btn.innerHTML = 'Generate Document';
            }, 1500);
        }
    });
}

// 1. Analyze
async function analyzeDocument() {
    const text = document.getElementById('analyze-input').value;
    const resultBox = document.getElementById('analyze-result');

    if (!text) { alert("Please enter text!"); return; }

    const response = await postData('/analyze', { text: text });
    resultBox.classList.remove('hidden');
    // Convert markdown (simple) to HTML ideally, but for now text
    // We replace newlines with <br> for basic formatting
    resultBox.innerHTML = formatOutput(response.analysis);
}

// 2. Simplify
async function simplifyDocument() {
    const text = document.getElementById('simplify-input').value;
    const resultBox = document.getElementById('simplify-result');

    if (!text) { alert("Please enter text!"); return; }

    const response = await postData('/simplify', { text: text });
    resultBox.classList.remove('hidden');
    resultBox.innerHTML = formatOutput(response.analysis);
}

// 3. Voice
async function translateVoice() {
    const text = document.getElementById('voice-input').value;
    const lang = document.getElementById('voice-lang').value;
    const resultBox = document.getElementById('voice-result');

    if (!text) { alert("Please enter text!"); return; }

    const response = await postData('/voice/translate', { text: text, target_language: lang });

    // Display Text
    resultBox.classList.remove('hidden');
    resultBox.innerHTML = `<p><strong>Translation (${lang}):</strong> <button class="icon-btn" onclick="speakText('${lang}')"><i class="fa-solid fa-volume-high"></i> Listen</button></p>` + formatOutput(response.analysis);

    // Speak Audio
    // We store the text to speak in a global variable or pass it, but simpler to just read from the response
    window.currentTranslation = response.analysis;
    speakText(lang);
}

function speakText(language) {
    if (!window.currentTranslation) return;

    // Using browser's built-in TTS (temporary - gTTS integration pending)
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(window.currentTranslation);

    const langMap = {
        'Spanish': 'es-ES', 'French': 'fr-FR', 'Hindi': 'hi-IN',
        'Tamil': 'ta-IN', 'Telugu': 'te-IN', 'Kannada': 'kn-IN',
        'Malayalam': 'ml-IN', 'Marathi': 'mr-IN', 'Bengali': 'bn-IN',
        'Gujarati': 'gu-IN', 'Punjabi': 'pa-IN',
        'Chinese': 'zh-CN', 'Arabic': 'ar-SA'
    };

    utterance.lang = langMap[language] || 'en-US';

    const voices = window.speechSynthesis.getVoices();
    const specificVoice = voices.find(v => v.lang.includes(utterance.lang));
    if (specificVoice) utterance.voice = specificVoice;

    window.speechSynthesis.speak(utterance);
}

// 4. Action
function updateTemplateForm() {
    const template = document.getElementById('template-select').value;
    const formGroup = document.getElementById('template-form');

    // Different templates need different fields
    const templates = {
        'parking_appeal_template.txt': `
            <input type="text" id="your-name" placeholder="Your Name">
            <input type="text" id="citation-number" placeholder="Citation Number">
            <input type="text" id="citation-date" placeholder="Date of Citation">
            <textarea id="user-story" placeholder="Explain why the ticket is unfair..."></textarea>
        `,
        'rental_dispute_template.txt': `
            <input type="text" id="your-name" placeholder="Your Name">
            <input type="text" id="landlord-name" placeholder="Landlord/Property Manager Name">
            <input type="text" id="property-address" placeholder="Property Address">
            <textarea id="user-story" placeholder="Describe the dispute and desired resolution..."></textarea>
        `,
        'medical_bill_dispute_template.txt': `
            <input type="text" id="your-name" placeholder="Your Name">
            <input type="text" id="account-number" placeholder="Account Number">
            <input type="text" id="bill-amount" placeholder="Disputed Amount">
            <textarea id="user-story" placeholder="Explain the billing error..."></textarea>
        `,
        'insurance_appeal_template.txt': `
            <input type="text" id="your-name" placeholder="Your Name">
            <input type="text" id="policy-number" placeholder="Policy Number">
            <input type="text" id="claim-number" placeholder="Claim Number">
            <textarea id="user-story" placeholder="Explain why the denial is incorrect..."></textarea>
        `,
        'consumer_complaint_template.txt': `
            <input type="text" id="your-name" placeholder="Your Name">
            <input type="text" id="company-name" placeholder="Company Name">
            <input type="text" id="order-number" placeholder="Order/Account Number">
            <textarea id="user-story" placeholder="Describe the issue and resolution requested..."></textarea>
        `,
        'employment_termination_dispute.txt': `
            <input type="text" id="your-name" placeholder="Your Name">
            <input type="text" id="employer-name" placeholder="Employer Name">
            <input type="text" id="termination-date" placeholder="Date of Termination">
            <textarea id="user-story" placeholder="Explain why you believe the termination was wrongful or unfair..."></textarea>
        `,
        'privacy_data_request.txt': `
            <input type="text" id="your-name" placeholder="Your Name">
            <input type="text" id="company-name" placeholder="Company Name">
            <textarea id="user-story" placeholder="Specify if you want to access, delete, or correct your data..."></textarea>
        `,
        'cease_and_desist_harassment.txt': `
            <input type="text" id="your-name" placeholder="Your Name">
            <input type="text" id="harasser-name" placeholder="Name of Harasser/Agency">
            <textarea id="user-story" placeholder="Describe the harassing behavior and specify you want all contact to stop..."></textarea>
        `,
        'security_deposit_refund.txt': `
            <input type="text" id="your-name" placeholder="Your Name">
            <input type="text" id="landlord-name" placeholder="Landlord Name">
            <input type="text" id="property-address" placeholder="Property Address">
            <input type="text" id="move-out-date" placeholder="Move-out Date">
            <textarea id="user-story" placeholder="Explain why you are entitled to the full refund..."></textarea>
        `,
        'unpaid_wages_demand.txt': `
            <input type="text" id="your-name" placeholder="Your Name">
            <input type="text" id="employer-name" placeholder="Employer Name">
            <input type="text" id="total-owed" placeholder="Total Amount Owed">
            <textarea id="user-story" placeholder="Describe the work performed and the period of non-payment..."></textarea>
        `,
        'nda_agreement_basic.txt': `
            <input type="text" id="disclosing-party" placeholder="Disclosing Party Name">
            <input type="text" id="receiving-party" placeholder="Receiving Party (You)">
            <textarea id="user-story" placeholder="Describe the confidential information being protected..."></textarea>
        `,
        'foia_request.txt': `
            <input type="text" id="your-name" placeholder="Your Name">
            <input type="text" id="agency-name" placeholder="Government Agency Name">
            <textarea id="user-story" placeholder="Describe the specific records or information you are requesting..."></textarea>
        `,
        'freelance_contract_dispute.txt': `
            <input type="text" id="your-name" placeholder="Your Name">
            <input type="text" id="client-name" placeholder="Client Name">
            <input type="text" id="invoice-number" placeholder="Invoice Number">
            <textarea id="user-story" placeholder="Explain the dispute over payment or deliverables..."></textarea>
        `
    };

    formGroup.innerHTML = templates[template] || templates['parking_appeal_template.txt'];
}

async function generateDocument() {
    const template = document.getElementById('template-select').value;
    const region = document.getElementById('region-select').value;
    const name = document.getElementById('your-name').value;
    const resultBox = document.getElementById('action-result');

    if (!name) { alert("Please fill in your name!"); return; }

    // Collect all input fields dynamically
    const inputs = document.querySelectorAll('#template-form input, #template-form textarea');
    const details = {};
    inputs.forEach(input => {
        const placeholder = input.placeholder.replace('...', '');
        details[placeholder] = input.value;
    });

    const response = await postData('/action/generate', {
        template_name: template,
        region: region,
        case_details: details
    });

    resultBox.classList.remove('hidden');
    resultBox.innerHTML = `<pre>${response.analysis}</pre>`;
}

function formatOutput(text) {
    if (!text) return "";

    let formatted = text;

    // Bold
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Headings (e.g., ### Heading or ## Heading)
    formatted = formatted.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    formatted = formatted.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    formatted = formatted.replace(/^# (.*$)/gim, '<h1>$1</h1>');

    // Bullet points (handle lines starting with * or -)
    formatted = formatted.replace(/^\* (.*$)/gim, '<li>$1</li>');
    formatted = formatted.replace(/^- (.*$)/gim, '<li>$1</li>');

    // Wrap lists in <ul> if <li> exists
    if (formatted.includes('<li>')) {
        // This is a simple logic: if we have <li>, we might need <ul>
        // For a more robust solution, a real markdown parser would be better
        // but this should help with the "red flags" and bulleted lists.
    }

    // Newlines to <br> (only if not inside a list or heading already? Actually let's just do it for simple lines)
    formatted = formatted.replace(/\n/g, '<br>');

    return formatted;
}
