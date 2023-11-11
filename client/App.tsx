import { StatusBar } from "expo-status-bar"
import { NativeWindStyleSheet } from "nativewind"
import { Text, View } from "react-native"

import { Hero } from "@/components/hero"

NativeWindStyleSheet.setOutput({
    default: "native",
})

export default function App() {
    return (
        <View className="flex-1 items-center justify-center">
            <Text className="font-bold text-red-500">
                Open up App.tsx to start working on your app!
            </Text>
            <Hero />
            <StatusBar style="auto" />
        </View>
    )
}
