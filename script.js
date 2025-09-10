console.log("hello");

import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm'

const SUPABASE_URL = 'https://vuftbtsbjzzoovmajyjn.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ1ZnRidHNianp6b292bWFqeWpuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc0Nzc4NTAsImV4cCI6MjA3MzA1Mzg1MH0.XWhNltdhYqYVQCWfzNsXJ1HVzDmZ3BqVPOCtkI4yKYQ';

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

console.log(supabase);




