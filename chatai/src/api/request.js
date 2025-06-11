
import axios from 'axios';

const BASE_RETRIEVE_URL = 'https://demo-trex.agentosaur.ai/api/v1/rag/retrieve_document';
const BASE_INDEX_URL = 'https://demo-trex.agentosaur.ai/index_document';

export const retrieveDocument = async (query) => {
  try {
    const response = await axios.post(
      BASE_RETRIEVE_URL,
      { query, mode: 'both' },
      { headers: { 'Content-Type': 'application/json' } }
    );
    return response.data;
  } catch (error) {
    console.error('Retrieve API Error:', error);
    throw error;
  }
};

export const uploadPDF = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const res = await fetch(BASE_INDEX_URL, {
      method: 'POST',
      body: formData,
    });

    return await res.json();
  } catch (err) {
    console.error('Upload PDF Error:', err);
    throw err;
  }
};
