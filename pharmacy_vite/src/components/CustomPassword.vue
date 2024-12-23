<template>
    <Password id="password" class="elements" toggleMask required>
        <template #header>
            <h6>Pick a password</h6>
        </template>
        <template #footer>
            <Divider />
            <p class="mt-2">Suggestions</p>
            <ul class="pl-2 ml-2 mt-0" style="line-height: 1.5">
                <li>At least one lowercase</li>
                <li>At least one uppercase</li>
                <li>At least one numeric</li>
                <li>Minimum 8 characters</li>
            </ul>
        </template>
    </Password>
</template>