import { useState, useEffect } from 'react';

function IndexPage() {
  const [analyses, setAnalyses] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [repoUrl, setRepoUrl] = useState('');

  useEffect(() => {
    fetch('http://127.0.0.1:5000/get_all_analysis')
      .then(response => response.json())
      .then(data => setAnalyses(data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  const handleCreateAnalysis = () => {
    fetch('http://127.0.0.1:5000/create_analysis', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ repo_url: repoUrl })
    })
      .then(response => response.json())
      .then(data => {
        setShowModal(false);
        // Update local state or re-fetch analysis list
        console.log('Analysis started:', data);
      })
      .catch(error => console.error('Error creating analysis:', error));
  };

  return (
    <div className='bg-light mg-0'>
    <ul className="container-sm text-center">
    
      {analyses.map(analysis => (
        <div className='w-100 border rounded bg-dark p-3 m-3'>
        <h1 className='text-light'>AA</h1>
      </div>
      ))}
    </ul>
    </div>
  );
}

export default IndexPage;
