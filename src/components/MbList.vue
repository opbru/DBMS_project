<template>
    <div class="container mt-5">
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
              <h1 class="text-center">Choose a Motherboard</h1>
            </div>
            <div class="card-body">
              <ul class="list-group">
                <li v-for="mb in mbs" :key="mb.id" class="list-group-item d-flex justify-content-between align-items-center">
                  <div>
                    <h5>{{ mb.name }}</h5>
                    <p>Price: ${{ mb.price }}</p>
                  </div>
                  <button class="btn btn-primary" @click="selectMb(mb.id)">Select</button>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  <script>
  import { getMbOptions, selectMb } from '../services/api';

  export default {
    data() {
      return {
        mbs: [],
        token: localStorage.getItem('token') || '',
        selectedCpu: JSON.parse(localStorage.getItem('selectedCpu')) || null,
      };
    },
    async created() {
      if (!this.selectedCpu) {
        this.$router.push('/get_cpu_options'); // Redirect to CPU list if CPU not selected
        return;
      }

      try {
        const response = await getMbOptions(this.selectedCpu.id, this.token);
        this.mbs = response.data;
        console.log("MB options fetched:", this.mbs); // Debug log
      } catch (error) {
        console.error('Failed to fetch MB options:', error);
      }
    },
    methods: {
      async selectMb(mbId) {
        try {
          await selectMb(mbId, this.token);
          alert('Motherboard selected successfully');
          localStorage.setItem('selectedMb', JSON.stringify({ id: mbId }));
          this.$router.push('/get_ram_options'); // Update this to the next step in your workflow
        } catch (error) {
          console.error('Failed to select Motherboard:', error);
          alert('Failed to select Motherboard');
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
  } </style>