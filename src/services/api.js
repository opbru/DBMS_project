// src/services/api.js

import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000'; // Replace with your Flask backend URL

export const register = (email, password) => {
    return axios.post(`${API_URL}/register`, {
        email,
        password
    });
};

export const login = (email, password) => {
    return axios.post(`${API_URL}/login`, {
        email,
        password
    });
};

export const setBudgetAndType = (budget, computer_type, token) => {
    return axios.post(`${API_URL}/set_budget_and_type`, {
      budget,
      computer_type
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
  };

export const getCpuOptions = (token) => {
    return axios.get(`${API_URL}/get_cpu_options`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
};

export const selectCpu = (cpuId, token) => {
    return axios.post(`${API_URL}/select_cpu/${cpuId}`, {}, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
};


export const getMbOptions = (cpuId, token) => {
    return axios.get(`${API_URL}/get_mb_options/${cpuId}`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
};

export const selectMb = (mbId, token) => {
    return axios.post(`${API_URL}/select_mb/${mbId}`, {}, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
};

export const getRamOptions = (mbId, token) => {
    return axios.get(`${API_URL}/get_ram_options/${mbId}`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
};

export const selectRam = (ramId, token) => {
    return axios.post(`${API_URL}/select_ram/${ramId}`, {}, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
};

export const getGpuOptions = (token) => {
    return axios.get(`${API_URL}/get_gpu_options`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
}

export const selectGpu = (gpuId, token) => {
    return axios.post(`${API_URL}/select_gpu/${gpuId}`, {}, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
}

export const getSsdOptions = (token) => {
    return axios.get(`${API_URL}/get_ssd_options`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
}

export const selectSsd = (ssdId, token) => {
    return axios.post(`${API_URL}/select_ssd/${ssdId}`, {}, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
}

export const getHddOptions = (token) => {
    return axios.get(`${API_URL}/get_hdd_options`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
}

export const selectHdd = (hddId, token) => {
    return axios.post(`${API_URL}/select_hdd/${hddId}`, {}, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
}

export const getPsuOptions = (token) => {
    return axios.get(`${API_URL}/get_psu_options`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
}

export const selectPsu = (psuId, token) => {
    return axios.post(`${API_URL}/select_psu/${psuId}`, {}, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
}

export const getChassisOptions = (mbId, gpuId,token) => {
    return axios.get(`${API_URL}/get_chassis_options/${mbId}/${gpuId}`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
}

export const selectChassis = (chassisId, token) => {
    return axios.post(`${API_URL}/select_chassis/${chassisId}`, {}, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
}

export const finalizeSelection = (token) => {
    return axios.post(`${API_URL}/finalize_selection`, {}, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
};

export const recommendGpu = (token) => {
    return axios.get(`${API_URL}/recommend_gpu`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
};