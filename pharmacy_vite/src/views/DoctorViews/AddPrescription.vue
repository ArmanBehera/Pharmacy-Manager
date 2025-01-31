<script setup>
    import '../../styles/styles.css';
    import axios from '../../axios';
    import { useStore } from 'vuex';
    import { ref, computed, watch } from 'vue';
    import { useToast } from 'primevue/usetoast';
    import { useRoute } from 'vue-router';
    import { AutoComplete, InputText } from 'primevue';

    const store = useStore();
    store.dispatch('initializeStore');

    const toast = useToast();
    const route = useRoute();

    const appointmentDetails = ref();
    const id =  route.query.id;

    const firstName = ref('');
    const lastName = ref('');
    const gender = ref('');
    const age = ref('');

    const medicineCount = ref(1);
    const medicinesData = ref([]);
    const prescribedMedicines = ref([]);
    const frequencyMedicines = ref([]);
    const durationMedicines = ref([]);
    const durationUnit = ref([]);
    const durationUnitChoices = ref(['Days', 'Months'])

    const timings = ref([]);
    const customTimingDescriptions = ref([]);

    const timingsChoices = ref(['Before Food', 'After Food', 'Custom'])

    const labTestCount = ref(1);
    const labTestsData = ref([])
    const prescribedLabTests = ref([]);


    const unlistedIndexArrayMedicine = ref([])
    const unlistedIndexArrayLabTests = ref([])

    const additionalInformation = ref();

    const warn = (severity, summary, detailed) => {
        toast.add({ severity: severity, summary: summary, detail: detailed, life: 3000 });
    }

    const isRegistered = ref(store.state.isRegistered)

    if (isRegistered.value === 'true') {
        axios.post('/doctor/getAppointmentDetail/', {
            'id': id
        })
        .then( (response) => {
            appointmentDetails.value = response.data;
            firstName.value = appointmentDetails.value.patient.first_name 
            lastName.value = appointmentDetails.value.patient.last_name
            gender.value = appointmentDetails.value.patient.gender === 'Male'? 'M' : 'F'
            age.value = appointmentDetails.value.patient.age 
        })
        .catch( (error) => {
            warn('warn', 'Error getting appointment details for the patient.', 'Please check the status of the server or try reloading.')
        })

        axios.get('/doctor/getMedicines/')
        .then( (response) => {
            medicinesData.value = response.data
        })
        .catch( (error) => {
            warn('warn', 'Error getting medicines data.', 'Please check the status of the server or try reloading.')
        })

        axios.get('/doctor/getLabTests/')
        .then( (response) => {
            labTestsData.value = response.data
        })
        .catch( (error) => {
            warn('warn', 'Error getting lab tests data.', 'Please check the status of the server or try reloading.')
        })
    } else {
        warn('warn', 'Please log in to access this page.', '')
    }

    const filteredArray = ref();

    const search = (event, fullArray) => {
        setTimeout(() => {
            if (!event.query.trim().length) {
                filteredArray.value = [...fullArray]
            } else {
                filteredArray.value = fullArray.filter((element) => {
                    return element.name.toLowerCase().startsWith(event.query.toLowerCase());
                });
            }
        }, 50);
    }

    // Computed function to check if a specific medicine is unlisted
    const isUnlistedMedicine = (index) => {
        return computed(() => {
            const selectedMedicine = prescribedMedicines.value[index];
            return selectedMedicine && !medicinesData.value.some(medicine => medicine.name === selectedMedicine.name);
        });
    };

    // Watch for changes in prescribedMedicines and update indexArrayMedicine
    watch(prescribedMedicines, (newMedicines) => {
        unlistedIndexArrayMedicine.value = newMedicines
            .map((medicine, index) => ({
                isUnlisted: medicine && !medicinesData.value.some(med => med.name === medicine.name),
                index,
            }))
            .filter(med => med.isUnlisted)
            .map(med => med.index);
    }, { deep: true });

    watch(prescribedLabTests, (newLabTests) => {
        unlistedIndexArrayLabTests.value = newLabTests
            .map((labTest, index) => ({
                isUnlisted: labTest && !labTestsData.value.some(lab => lab.name === labTest.name),
                index,
            }))
            .filter(med => med.isUnlisted)
            .map(med => med.index);
    }, { deep: true });


    const submit = () => {
        const listedMedicines = ref([])
        const listedLabTests = ref([])

        const unlistedMedicines = ref([])
        const unlistedLabTests = ref([])

        // Need to refactor timings and their choices

        for (let i = 0; i < medicineCount.value; i++) {
            if (unlistedIndexArrayMedicine.value.some(index => index === i)) {
                unlistedMedicines.value.push({'medicine': prescribedMedicines.value[i], 'frequency': frequencyMedicines.value[i], 'duration': durationMedicines.value[i], 'durationUnit': durationUnit.value[i], 'timings': timings.value[i], 'customTimingDescription': customTimingDescriptions.value[i]})
            } else {
                listedMedicines.value.push({'medicine': prescribedMedicines.value[i], 'frequency': frequencyMedicines.value[i], 'duration': durationMedicines.value[i], 'durationUnit': durationUnit.value[i]})
            }
        }

        for (let i = 0; i < labTestCount.value; i++) {
            if (unlistedIndexArrayLabTests.value.some(index => index === i)) {
                unlistedLabTests.value.push({'labTest': prescribedLabTests.value[i]});
            } else {
                listedLabTests.value.push(prescribedLabTests.value[i]);
            }
        }

        const prescriptionToSend = {
            'appointmentId': appointmentDetails.value.id,
            'medicines': listedMedicines.value,
            'labTests': listedLabTests.value,
            'unlistedMedicines': unlistedMedicines.value,
            'unlistedLabTests': unlistedLabTests.value,
            'additionalInformation': additionalInformation.value
        }

        axios.post('/doctor/addPrescription/', {
            ...prescriptionToSend
        })
        .then( (response) => {
            warn('success', 'Successfully added prescription for the patient.', '')
        })
        .catch( (error) => {
            warn('warn', 'Unsuccessful in adding prescription for the patient.', 'Please check the status of the server or try reloading.')
        })
    }
</script>

<template>
    <Toast/>

    <div class="centered" v-if="isRegistered === 'true'">
        <h1 class="text-3xl font-bld m-3">Prescription for {{ firstName }} {{ lastName }} ({{ age }}{{ gender }})</h1>
    </div>


    <div class="container mx-auto flex flex-column" v-if="isRegistered === 'true'">
        <div class="flex flex-col space-y-4">
            <label class="text-2xl font-semibold">Medicines</label>
            <div v-for="n in medicineCount" :key="n" class="flex flex-row items-center space-x-4">
                <AutoComplete :placeholder="`Medicine ${n}*`" v-model="prescribedMedicines[n - 1]" optionLabel="name" dropdown :suggestions="filteredArray" @complete="(event) => search(event, medicinesData )" class="w-full" />
                <InputNumber id="frequency" placeholder="Frequency *" inputId="withoutgrouping" :useGrouping="false" v-model.number="frequencyMedicines[n-1]" :min="0" class="p-inputnumber-sm w-full"/>
                <InputNumber id="duration" placeholder="Duration *" inputId="withoutgrouping" :useGrouping="false" v-model.number="durationMedicines[n-1]" :min="0" class="p-inputnumber-sm w-full"/>
                <Select v-model="durationUnit[n - 1]" :options="durationUnitChoices" placeholder="Unit *"/>
                <Select v-model="timings[n - 1]" :options="timingsChoices" placeholder="Timing for taking the medicine *" v-if="isUnlistedMedicine(n - 1).value"/>
                <Select v-model="timings[n - 1]" :options="timingsChoices" placeholder="Timing for taking the medicine" v-else disabled/>
                <InputText v-model.trim="customTimingDescriptions[n - 1]" id="customTiming" placeholder="Custom Timing Description *" v-if="timings[n - 1] === 'Custom'" class="p-inputtext-sm w-full"/>
            </div>
            <div>
                <Button label="Add Medicine" @click.prevent="medicineCount += 1"/>
                <Button label="Delete Medicine" severity="danger" @click.prevent="medicineCount = medicineCount > 1 ? medicineCount - 1 : medicineCount" class="ml-4"/>
            </div>
        </div>

        <div class="flex flex-col space-y-4 mt-4">
            <label class="text-2xl font-semibold">Lab Tests</label>
            <div v-for="n in labTestCount" :key="n" class="flex flex-row justify-content-center align-items-center space-x-4">
                <AutoComplete :placeholder="`Lab Test ${n}`" v-model="prescribedLabTests[n - 1]" optionLabel="name" dropdown :suggestions="filteredArray" @complete="(event) => search(event, labTestsData )" class="w-full" />
            </div>
            <div>
                <Button label="Add Lab Test" @click.prevent="labTestCount += 1"/>
                <Button label="Delete Lab Test" severity="danger" @click.prevent="labTestCount = labTestCount > 1 ? labTestCount - 1 : labTestCount" class="ml-4"/>
            </div>
        </div>

        <div class="flex flex-col spaace-y-4 mt-4">
            <label class="text-2xl font-semibold">Additional Information</label>
            <InputText v-model.trim="additionalInformation" id="additionalInformation" placeholder="Additional Information" class="mt-2 p-inputtext-sm w-full"/>
        </div>

        <div class="flex justify-content-center align-items-center mt-4">
            <Button severity="success" label="Submit" @click.prevent="submit" v-if="isRegistered === 'true'"/>
            <Button severity="danger" label="Submit" disabled v-else/>
        </div>
    </div>
</template>