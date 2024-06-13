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
              <h1 class="text-center">Choose an SSD</h1>
            </div>
            <div class="card-body">
              <ul class="list-group">
                <li v-for="ssd in ssds" :key="ssd.id" class="list-group-item d-flex justify-content-between align-items-center">
                  <div>
                    <h5>{{ ssd.name }}</h5>
                    <p>Price: ${{ ssd.price }}</p>
                  </div>
                  <button class="btn btn-primary" @click="selectSsd(ssd.id)">Select</button>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  <script>
  import { getSsdOptions, selectSsd } from '../services/api';

  export default {
    data() {
      return {
        ssds: [],
        token: localStorage.getItem('token') || '',
      };
    },
    async created() {
      try {
        const response = await getSsdOptions(this.token);
        this.ssds = response.data;
        console.log("SSD options fetched:", this.ssds); // Debug log
      } catch (error) {
        console.error('Failed to fetch SSD options:', error);
      }
    },
    methods: {
      async selectSsd(ssdId) {
        try {
          await selectSsd(ssdId, this.token);
          alert('SSD selected successfully');
          localStorage.setItem('selectedSsd', JSON.stringify({ id: ssdId }));
          this.$router.push('/get_hdd_options'); // Update this to the next step in your workflow
        } catch (error) {
          console.error('Failed to select SSD:', error);
          alert('Failed to select SSD');
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