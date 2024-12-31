// JavaScript Frontend for Feedback Application

const apiUrl = 'http://127.0.0.1:5000';


//async function apiRequest(url, method = 'GET', data = null, headers = {}) {
//    try {
//        const options = {
//            method: method.toUpperCase(),
//            headers: {
//                'Content-Type': 'application/json',
//                ...headers
//            }
//        };
//
//        if (method.toUpperCase() === 'POST' && data) {
//            options.body = JSON.stringify(data);
//        }
//
//        const response = await fetch(url, options);
//
//        if (!response.ok) {
//            throw new Error(`HTTP error! Status: ${response.status}`);
//        }
//
//        const responseData = await response.json();
//        return responseData;
//    } catch (error) {
//        console.error(`Error with ${method} request to ${url}:`, error);
//        throw error;
//    }
//}


// Utility to make API requests
async function apiRequest(endpoint, method = 'GET', data = null) {
    const options = {
        method,
            headers: {
                'Content-Type': 'application/json',
            },
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    const response = await fetch(`${apiUrl}${endpoint}`, options);
    console.log(response)
    return response.json();
}

// Register a new user
async function register(email) {
const result = await apiRequest('/register', 'POST', { 'email' : email });
console.log('result');
console.log(result.status);
if(result.status == 'Yes'){
    window.location.assign("verify_otp");
}else{
    alert('invalid email');
}

}

// Verify user email with OTP
async function verifyEmail(email, otp) {
    console.log(email);
    const result = await apiRequest('/verify', 'POST', { 'email': email, 'otp': otp });
    if(result.status == 'Yes'){
        alert(json(result))
        window.location.assign("received_feedbacks");
    }else{
        alert(result)
    }
}

// Login user with OTP
async function login(email) {
const result = await apiRequest('/login', 'POST', { email });
alert(result.message);
}

// Send feedback
async function sendFeedback(senderId, recipientEmail, content) {
const result = await apiRequest('/send_feedback', 'POST', {
sender_id: senderId,
recipient_email: recipientEmail,
content,
});
alert(result.message);
}

// Get feedbacks received by the user
async function getReceivedFeedbacks(userId) {
const feedbacks = await apiRequest(`/received_feedbacks/${userId}`);
console.log(feedbacks);
}

// Update feedback status
async function updateFeedbackStatus(feedbackId, status) {
const result = await apiRequest('/update_feedback_status', 'POST', {
feedback_id: feedbackId,
status,
});
alert(result.message);
}

// Reply to a feedback
async function replyFeedback(feedbackId, reply) {
const result = await apiRequest('/reply_feedback', 'POST', {
                        feedback_id: feedbackId,
                        reply,
                    });
alert(result.message);
}

// Event handlers for the UI
function setupEventHandlers() {
    const registerBtn = document.getElementById('registerBtn');
    if(registerBtn){
        registerBtn.addEventListener('click', () => {
            const email = document.getElementById('registerEmail').value;
            register(email);
        });
    }

    const verifyBtn = document.getElementById('verifyBtn');
    if(verifyBtn){
        verifyBtn.addEventListener('click', () => {

            const email = document.getElementById('verifyEmail').value;
            const otp = document.getElementById('verifyOtp').value;
            verifyEmail(email, otp);
        });
     }

//document.getElementById('loginBtn').addEventListener('click', () => {
//const email = document.getElementById('loginEmail').value;
//login(email);
//});

    const sendFeedbackBtn = document.getElementById('sendFeedbackBtn');
    if(sendFeedbackBtn){
        sendFeedbackBtn.addEventListener('click', () => {
            const senderId = document.getElementById('senderId').value;
            const recipientEmail = document.getElementById('recipientEmail').value;
            const content = document.getElementById('feedbackContent').value;
            sendFeedback(senderId, recipientEmail, content);
        });
    }
}

// Initialize the application
window.onload = setupEventHandlers;
