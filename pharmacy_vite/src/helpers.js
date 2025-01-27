// Returns true if the date is today or before today, true otherwise
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

// Returns true if the date is today.
export const checkToday = (date) => {
    if (!date || !date.value) {
        return false;
    }

    const inputDate = new Date(date.value);
    const today = new Date();

    // Reset hours, minutes, seconds, and milliseconds for comparison
    inputDate.setHours(0, 0, 0, 0);
    today.setHours(0, 0, 0, 0);

    // Compare the two dates
    return inputDate.getTime() === today.getTime();
};


export const convertDateFormat = (dateString) => {
    // Split the date string by the hyphen
    const [year, month, day] = dateString.split('-');
    // Reorder the parts and join with a hyphen
    return `${day}-${month}-${year}`;
};