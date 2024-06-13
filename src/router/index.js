import { createRouter, createWebHistory } from 'vue-router';
import Register from '../components/UserRegister.vue';
import Login from '../components/UserLogin.vue';
import SelectBudgetAndType from '../components/SelectBudgetAndType.vue';
import CpuList from '../components/CpuList.vue';
import MbList from '../components/MbList.vue';
import RamList from '../components/RamList.vue';
import SsdList from '../components/SsdList.vue';
import HddList from '../components/HddList.vue';
import GpuList from '../components/GpuList.vue';
import PsuList from '../components/PsuList.vue';
import ChassisList from '../components/ChassisList.vue';
import FinalSelection from '../components/FinalSelection.vue';
// import AuthenticatedLayout from '../layout/AuthenticaticLayout.vue';
// import HelloWorld from '../components/HelloWorld.vue';

// Import other components as needed

const routes = [
  // { path: '/', component: HelloWorld },
  { path: '/register', component: Register },
  { path: '/login', component: Login },
  { path: '/set_budget_and_type', component: SelectBudgetAndType, meta: { requiresAuth: true } },
  { path: '/get_cpu_options', component: CpuList, meta: { requiresAuth: true } },
  { path: '/get_mb_options', component: MbList, meta: { requiresAuth: true } },
  { path: '/get_ram_options', component: RamList, meta: { requiresAuth: true } },
  { path: '/get_ssd_options', component: SsdList, meta: { requiresAuth: true } },
  { path: '/get_hdd_options', component: HddList, meta: { requiresAuth: true } },
  { path: '/get_gpu_options', component: GpuList, meta: { requiresAuth: true } },
  { path: '/get_psu_options', component: PsuList, meta: { requiresAuth: true } },
  { path: '/get_chassis_options', component: ChassisList, meta: { requiresAuth: true } },
  { path: '/finalize_selection', component: FinalSelection, meta: { requiresAuth: true } },
  // { path: '/', component: AuthenticatedLayout, meta: { requiresAuth: true },
  //   children: [{
  //     path: 'set_budget_and_type',
  //     component: SelectBudgetAndType,
  //   }]
  // },
  // Add routes for other components
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token');
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router;
