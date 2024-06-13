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
              <h1 class="text-center">Choose RAM</h1>
            </div>
            <div class="card-body">
              <ul class="list-group">
                <li v-for="ram in rams" :key="ram.id" class="list-group-item d-flex justify-content-between align-items-center">
                  <div>
                    <h5>{{ ram.name }}</h5>
                    <p>Price: ${{ ram.price }}</p>
                  </div>
                  <button class="btn btn-primary" @click="selectRam(ram.id)">Select</button>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  <script>
  import { getRamOptions, selectRam } from '../services/api';

  export default {
    data() {
      return {
        rams: [],
        token: localStorage.getItem('token') || '',
        selectedMb: JSON.parse(localStorage.getItem('selectedMb')) || null,
      };
    },
    async created() {
      if (!this.selectedMb) {
        this.$router.push('/get_mb_options'); // Redirect to MB list if MB not selected
        return;
      }

      try {
        const response = await getRamOptions(this.selectedMb.id, this.token);
        this.rams = response.data;
        console.log("RAM options fetched:", this.rams); // Debug log
      } catch (error) {
        console.error('Failed to fetch RAM options:', error);
      }
    },
    methods: {
      async selectRam(ramId) {
        try {
          await selectRam(ramId, this.token);
          alert('RAM selected successfully');
          localStorage.setItem('selectedRam', JSON.stringify({ id: ramId }));
          this.$router.push('/get_SSD_options'); // Update this to the next step in your workflow
        } catch (error) {
          console.error('Failed to select RAM:', error);
          alert('Failed to select RAM');
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
    }
</style>