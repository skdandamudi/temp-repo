const express = require('express');
const axios = require('axios');
const sqlite3 = require('sqlite3').verbose();
const nodemailer = require('nodemailer');
const app = express();
const port = 3000;

 
const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: 'youremail@gmail.com',
      pass: 'yourpassword'
    }
  });
// Initialize SQLite database
let db = new sqlite3.Database('./monitor.db', (err) => {
  if (err) {
    console.error('Error opening database:', err.message);
  } else {
    // Create the table if it doesn't exist
    db.run(`
      CREATE TABLE IF NOT EXISTS website_status (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        status TEXT,
        timestamp DATETIME DEFAULT (datetime('now','localtime'))
      )
    `);
  }
});

// Middleware to serve static files (like CSS)
app.use(express.static('public'));

// Endpoint to retrieve website status
app.get('/status', (req, res) => {
  db.all('SELECT * FROM website_status ORDER BY timestamp DESC LIMIT 10', [], (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message });
    } else {
      res.json(rows);
    }
  });
});


  
  var mailOptions = {
    from: 'youremail@gmail.com',
    to: 'myfriend@yahoo.com',
    subject: 'Sending Email using Node.js',
    text: 'That was easy!'
  };
  
  transporter.sendMail(mailOptions, function(error, info){
    if (error) {
      console.log(error);
    } else {
      console.log('Email sent: ' + info.response);
    }
  });

// Function to monitor websites
const websites = ['https://www.example.com', 'https://www.google.com'];

const monitorWebsites = () => {
  websites.forEach(async (website) => {
    try {
        console.log('fetching:',website );
      const response = await axios.get(website);
      const status = response.status === 200 ? 'UP' : 'DOWN';
      saveStatusToDb(website, status);
    } catch (error) {
      saveStatusToDb(website, 'DOWN');

      
    }
  });
};

// Function to save status to the database
const saveStatusToDb = (url, status) => {
  db.run('INSERT INTO website_status (url, status) VALUES (?, ?)', [url, status], (err) => {
    if (err) {
      console.error('Error saving to database:', err.message);
    }
  });
};

// Monitor websites every 5 minutes
setInterval(monitorWebsites, 1 * 60 * 1000);  // 5 minutes in milliseconds

// Serve the webpage
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
