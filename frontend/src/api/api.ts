import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const analyzeRepo = async (repoUrl) => {
  const response = await API.post("/analyze-repo", {
    repo_url: repoUrl,
  });
  return response.data;
};