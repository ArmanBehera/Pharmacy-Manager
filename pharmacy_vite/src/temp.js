

axios.post("/administrator/verifyEmployees/", { code: code, ids: idArray })
.then( (response) => {
    data.value = data.value.filter(val => !selected.value.includes(val));
    selected.value = null;

    if (code == 0){
        toast.add({severity:'success', summary: 'Successfully verified users!', life: 3000});
    } else {
        toast.add({severity:'success', summary: 'Successfully deleted users!', life: 3000});
    }
})
.catch( (error) => {
    console.log(error)
    if (code == 0){
        toast.add({severity:'warn', summary: 'Unsuccesful in verifying users.', message: 'Please try again.', life:3000});
    } else {
        toast.add({severity:'warn', summary: 'Unsuccesful in deleting users.', message: 'Please try again.', life:3000});
    }
})