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
              <h1 class="text-center">Choose a Chassis</h1>
            </div>
            <div class="card-body">
              <ul class="list-group">
                <li v-for="chassis in chassisList" :key="chassis.id" class="list-group-item d-flex justify-content-between align-items-center">
                  <div>
                    <h5>{{ chassis.name }}</h5>
                    <p>Price: ${{ chassis.price }}</p>
                  </div>
                  <button class="btn btn-primary" @click="selectChassis(chassis.id)">Select</button>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  <script>
  import { getChassisOptions, selectChassis } from '../services/api';

  export default {
    data() {
      return {
        chassisList: [],
        token: localStorage.getItem('token') || '',
        mbId: localStorage.getItem('selectedMb') ? JSON.parse(localStorage.getItem('selectedMb')).id : null,
        gpuId: localStorage.getItem('selectedGpu') ? JSON.parse(localStorage.getItem('selectedGpu')).id : null,
      };
    },
    async created() {
      try {
        if (!this.mbId || !this.gpuId) {
          alert('Motherboard or GPU not selected');
          this.$router.push('/get_gpu_options'); // Redirect to the previous step
        }

        const response = await getChassisOptions(this.mbId, this.gpuId, this.token);
        this.chassisList = response.data;
        console.log("Chassis options fetched:", this.chassisList); // Debug log
      } catch (error) {
        console.error('Failed to fetch chassis options:', error);
      }
    },
    methods: {
      async selectChassis(chassisId) {
        try {
          await selectChassis(chassisId, this.token);
          alert('Chassis selected successfully');
          localStorage.setItem('selectedChassis', JSON.stringify({ id: chassisId }));
          this.$router.push('/finalize_selection'); // Update this to the next step in your workflow
        } catch (error) {
          console.error('Failed to select chassis:', error);
          alert('Failed to select chassis');
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