<template>
    <div class="container mt-5">
      <div class="row">
      <div class="row justify-content-center">
        <div class="col-md-3">
        <div class="state-panel">
          <div class="state-circle-f">Budget selection</div>
          <div class="state-circle-t">Component selection</div>
          <div class="state-circle-f">Result</div>
        </div>
      </div>
        <div class="col-md-8">
          <div class="card">
            <div class="card-header">
              <h1 class="text-center">Choose a CPU</h1>
            </div>
            <div class="card-body">
              <ul class="list-group">
                <li v-for="cpu in cpus" :key="cpu.id" class="list-group-item d-flex justify-content-between align-items-center">
                  <div>
                    <h5>{{ cpu.name }}</h5>
                    <p>Price: ${{ cpu.price }}</p>
                    <p>Benchmark: {{ cpu.benchmark }}</p>
                  </div>
                  <button class="btn btn-primary" @click="selectCpu(cpu.id)">Select</button>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>
  </template>
0
  <script>
  import { getCpuOptions, selectCpu } from '../services/api';

  export default {
    data() {
      return {
        cpus: [],
        token: localStorage.getItem('token') || '',
      };
    },
    async created() {
      try {
        const response = await getCpuOptions(this.token);
        this.cpus = response.data;
        console.log("CPU options fetched:", this.cpus); // Debug log
      } catch (error) {
        console.error('Failed to fetch CPU options:', error);
      }
    },
    methods: {
      async selectCpu(cpuId) {
        try{
          await selectCpu(cpuId, this.token);
          alert('CPU selected successfully');
          localStorage.setItem('selectedCpu', JSON.stringify({ id: cpuId }));
          this.$router.push('/get_mb_options'); // Update this to the next step in your workflow
        } catch (error) {
          console.error('Failed to select CPU:', error);
          alert('Failed to select CPU');
        }
      },
    },
  };
  </script>

  <style scoped>
  .container {
    display: flex;
    flex-direction: row;
  }  
  .col-md-3{
    background-color: #aaaaaa;
    height: fit-content;
    width: fit-content;
    border-radius: 50px;
  }
  
  .state-panel {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 10px;
  }
  
  .state-circle-t {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background-color: #34495e;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: bold;
    margin-bottom: 20px;
  }
  .state-circle-f {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background-color: #666666;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: bold;
    margin-bottom: 20px;
  }  </style>
