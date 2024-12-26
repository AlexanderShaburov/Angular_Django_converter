
const retrieveData = () => {
    const DATA_SERVER_URL = 'http://127.0.0.1:8000/db/gather_data/'
    
    fetch(DATA_SERVER_URL)
    .then(r => r.json())
    .then(d => console.log(d))
}
const getCSRFToken = ()=>{
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : ''
}

const testToken = () => {
    const TEST_URL = 'http://127.0.0.1:8000/api/test/';
    console.log('TEST_URL', TEST_URL);
    console.log('csrf token: ', getCSRFToken());
    fetch(TEST_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
        },
        credentials: 'include',
        body: JSON.stringify({'test': 'lets see!'})
    })
    .then(r=>r.json())
    .then(d=>{
        console.log('response for POST: ', d);
    });
}