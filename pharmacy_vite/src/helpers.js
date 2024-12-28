export const checkDate = (date) => {
    if (!date.value) {
        return false;
    } else {
        date = new Date(date.value);

        const currentDate = new Date();
        currentDate.setHours(0, 0, 0, 0);

        if (date < currentDate) {
            return false;
        }
    }

    return true;
}