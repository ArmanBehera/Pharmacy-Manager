<template>
    <div class="card">
        <Carousel :value="options" :numVisible="1" :numScroll="1" circular :autoplayInterval="10000">
            <template #item="slotProps">
                <div class="relative border border-surface-200 dark:border-surface-700 rounded m-2 p-4 bg-cover bg-center">
                    <div class="flex flex-column items-center justify-center h-full">
                        <div class="text-white text-2xl p-4 rounded">{{ slotProps.data.name }}</div>
                        <div class="mt-10 text-l">{{ slotProps.data.description }}</div>
                        <span class="mt-5">
                            <Button icon="pi pi-sign-in" severity="secondary" label="Sign In" @click.prevent="$router.push({ name: slotProps.data.siginroute })" v-if="slotProps.data.siginroute"/>
                            <Button icon="pi pi-user" label="Log In" class="ml-4" @click.prevent="$router.push({ name: slotProps.data.loginroute })"/>
                        </span>
                    </div>
                </div>
            </template>
        </Carousel>
    </div>
</template>