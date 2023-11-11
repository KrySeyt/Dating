import { StatusBar } from 'expo-status-bar';
import { Text, View } from 'react-native';
import { NativeWindStyleSheet } from 'nativewind';

NativeWindStyleSheet.setOutput({
	default: 'native',
});

export default function App() {
	return (
		<View className='flex-1 items-center justify-center'>
			<Text className='text-red-500 font-bold'>
				Open up App.tsx to start working on your app!
			</Text>
			<StatusBar style='auto' />
		</View>
	);
}
