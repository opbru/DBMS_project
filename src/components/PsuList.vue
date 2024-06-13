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
              <h1 class="text-center">Choose a PSU</h1>
            </div>
            <div class="card-body">
              <ul class="list-group">
                <li v-for="psu in psus" :key="psu.id" class="list-group-item d-flex justify-content-between align-items-center">
                  <div>
                    <h5>{{ psu.name }}</h5>
                    <p>Price: ${{ psu.price }}</p>
                  </div>
                  <button class="btn btn-primary" @click="selectPsu(psu.id)">Select</button>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  <script>
  import { getPsuOptions, selectPsu } from '../services/api';

  export default {
    data() {
      return {
        psus: [],
        token: localStorage.getItem('token') || '',
      };
    },
    async created() {
      try {
        const response = await getPsuOptions(this.token);
        this.psus = response.data;
        console.log("PSU options fetched:", this.psus); // Debug log
      } catch (error) {
        console.error('Failed to fetch PSU options:', error);
      }
    },
    methods: {
      async selectPsu(psuId) {
        try {
          await selectPsu(psuId, this.token);
          alert('PSU selected successfully');
          localStorage.setItem('selectedPsu', JSON.stringify({ id: psuId }));
          this.$router.push('/get_chassis_options'); // Update this to the next step in your workflow
        } catch (error) {
          console.error('Failed to select PSU:', error);
          alert('Failed to select PSU');
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