// Returns true if the date is today or before today, true otherwise
export const checkDate = (date) => {
    if (!date.value) {
        return false;
    } else {
        date = new Date(date.value);

        const current_date = new Date();
        current_date.setHours(0, 0, 0, 0);

        if (date < current_date) {
            return false;
        }
    }

    return true;
}

// Returns true if the date is today.
export const checkToday = (date) => {
    if (!date && !date.value) {
        return false;
    }

    const input_date = new Date(date);
    const today = new Date();

    // Reset hours, minutes, seconds, and milliseconds for comparison
    input_date.setHours(0, 0, 0, 0);
    today.setHours(0, 0, 0, 0);

    // Compare the two dates
    return input_date.getDate() === today.getDate();
};


export const convertDateFormat = (date_string) => {
    // Split the date string by the hyphen
    const [first, second, third] = date_string.split('-');
    // Reorder the parts and join with a hyphen
    return `${third}-${second}-${first}`;
};

export const capitalize = (string) => {
    return string.charAt(0).toUpperCase() + string.slice(1)
}

export const filled = (data, optional_fields) => {

    for (const key in data) {
        if (!optional_fields.includes(key)) {
            const value = data[key];
            if (typeof value === 'string' && value.trim() === '') {
                return key; // Exit the loop early if an empty field is found
            } else if (typeof value === 'number' && value === 0) {
                return key; // Exit the loop early if a zero value is found
            } else if (Array.isArray(value) && value.length === 0) {
                return key;
            }
        }
    }

    return 'success';
}