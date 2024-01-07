SUCCESS_CODE = 'success'
ERROR_CODE = 'error'


async function fetch_data_by_get(url) {
    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP请求失败，状态码: ${response.status}`);
        }

        const res = await response.json();

        if (res.status === ERROR_CODE) {
            throw new Error('请求成功，但是发生错误：' + res.error_message);
        }

        if (res.status === SUCCESS_CODE) {
            return res.data;
        }

        console.warn('未处理的状态码:', res.status);
    } catch (error) {
        console.error('请求发生错误:', error);
        throw error; // 如果需要在外部处理错误，可以将错误抛出
    }
}
