import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura'
import './styles/tailwind.css';

// Importing PrimeVue components
import InputText from 'primevue/inputtext';
import DatePicker from 'primevue/datepicker';
import Button from 'primevue/button';
import FloatLabel from 'primevue/floatlabel';
import Password from 'primevue/password';
import InputNumber from 'primevue/inputnumber';
import Select from 'primevue/select';
import Divider from 'primevue/divider';
import Menubar from 'primevue/menubar';
import Toast from 'primevue/toast';
import ToastService from 'primevue/toastservice';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Toolbar from 'primevue/toolbar';
import Dialog from 'primevue/dialog';
import Row from 'primevue/row';
import Drawer from 'primevue/drawer';
import Textarea from 'primevue/textarea';
import AutoComplete from 'primevue/autocomplete';
import Carousel from 'primevue/carousel';

// Importing Custom components
import CustomPassword from './components/CustomPassword.vue';

import 'primeicons/primeicons.css';
import 'primeflex/primeflex.css';

const app = createApp(App);

app.use(PrimeVue, {
    theme: {
         preset: Aura,
         options: {
            prefix: 'p',
            darkModeSelector: 'system',
            cssLayer: false
         }
    }
});

app.component('InputText', InputText);
app.component('DatePicker', DatePicker);
app.component('Button', Button);
app.component('FloatLabel', FloatLabel);
app.component('Divider', Divider);
app.component('Password', Password);
app.component('InputNumber', InputNumber);
app.component('Select', Select);
app.component('Menubar', Menubar);
app.component('Toast', Toast);
app.component('DataTable', DataTable);
app.component('Column', Column);
app.component('Toolbar', Toolbar);
app.component('Dialog', Dialog);
app.component('Row', Row);
app.component('Drawer', Drawer);
app.component('Textarea', Textarea);
app.component('AutoComplete', AutoComplete);
app.component('Carousel', Carousel);

app.component('CustomPassword', CustomPassword);

app.use(store);
app.use(router);
app.use(ToastService);

app.mount('#app');
