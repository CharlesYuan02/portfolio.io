import "./CreateUsername.css";
import React, { useState } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { useNavigate } from 'react-router-dom';
import { createClient } from '@supabase/supabase-js';

const supabaseURL = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_API_KEY;
const usersTable = process.env.REACT_APP_SUPABASE_USERS_TABLE;
const supabase = createClient(supabaseURL, supabaseKey);

const CreateUsername = () => {
    const [username, setUsername] = useState('');
    const [confirmUsername, setConfirmUsername] = useState('');
    const [error, setError] = useState('');
    const { user } = useAuth0();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        // Get existing list of usernames from Supabase to ensure uniqueness
        const { data: existingUsernames, error: usernameError } = await supabase
            .from(usersTable)
            .select('username');
        console.log('Existing usernames:', existingUsernames);
        
        if (usernameError) {
            console.error('Error fetching existing usernames:', usernameError);
            setError('Could not fetch existing usernames. Please try again later.');
        }

        if (username !== confirmUsername) {
            setError('Usernames must match!');
            return;
        } else if (existingUsernames.some((user) => user.username === username)) {
            setError('Username already exists!');
            return;
        } else {
            console.log("Username submitted:", username);
        }

        const { email, sub } = user;
        try {
            const { data, error } = await supabase
                .from(usersTable)
                .insert([
                    { 
                        email: email,
                        password: sub,
                        username: username,
                    }
                ]);

            if (error) throw error;
            console.log('User data stored successfully:', data);
            navigate('/dashboard'); // Redirect to dashboard

        } catch (error) {
            console.error('Error storing user data:', error);
            setError('Could not store user into database. Please try again later.');
        }
    };

    return (
        <div className="page-container">
            <form onSubmit={handleSubmit} className="form-container">
                <div className="input-container">
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Choose a username"
                        required
                    />
                </div>
                <div className="input-container">
                    <input
                        type="text"
                        value={confirmUsername}
                        onChange={(e) => setConfirmUsername(e.target.value)}
                        placeholder="Confirm username"
                        required
                    />
                </div>
                {error && <p className="error-message">{error}</p>}
                <button type="submit" className="submit-button">Create Username</button>
            </form>
        </div>
    );
};

export default CreateUsername;