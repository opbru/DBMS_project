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
              <h1 class="text-center">Choose an HDD</h1>
            </div>
            <div class="card-body" v-if="hddRatio > 0">
              <ul class="list-group">
                <li v-for="hdd in hdds" :key="hdd.id" class="list-group-item d-flex justify-content-between align-items-center">
                  <div>
                    <h5>{{ hdd.name }}</h5>
                    <p>Price: ${{ hdd.price }}</p>
                  </div>
                  <button class="btn btn-primary" @click="selectHdd(hdd.id)">Select</button>
                </li>
              </ul>
            </div>
            <div v-else>
              <p>No budget allocated for HDD.</p>
              <button class="btn btn-primary" @click="skipHdd">Skip HDD Selection</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  <script>
  import { getHddOptions, selectHdd } from '../services/api';

  export default {
    data() {
      return {
        hdds: [],
        token: localStorage.getItem('token') || '',
        hddRatio: 1, // Default value, will be updated based on API response
      };
    },
    async created() {
      try {
        const response = await getHddOptions(this.token);
        this.hdds = response.data;
        console.log("HDD options fetched:", this.hdds); // Debug log

        // Determine hddRatio based on fetched options
        if (this.hdds.length === 0) {
          this.hddRatio = 0;
        }
      } catch (error) {
        console.error('Failed to fetch HDD options:', error);
      }
    },
    methods: {
      async selectHdd(hddId) {
        try {
          await selectHdd(hddId, this.token);
          alert('HDD selected successfully');
          localStorage.setItem('selectedHdd', JSON.stringify({ id: hddId }));
          this.$router.push('/get_gpu_options'); // Update this to the next step in your workflow
        } catch (error) {
          console.error('Failed to select HDD:', error);
          alert('Failed to select HDD');
        }
      },
      skipHdd() {
        localStorage.setItem('selectedHdd', JSON.stringify({ id: null }));
        this.$router.push('/get_gpu_options'); // Update this to the next step in your workflow
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