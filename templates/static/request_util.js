SUCCESS_CODE = 'success'
ERROR_CODE = 'error'


async function fetchData(url) {
    try {
        const response = await fetch(url);
        var res = await response.json()
        if (res.status === ERROR_CODE) {
            throw new Error('请求成功，但是发生错误');
        }
        if (res.status === SUCCESS_CODE) {
            return res.data;
        }
        // return response.json();
    } catch (error) {
        console.error('请求发生错误:', error);
        throw error; // 如果需要在外部处理错误，可以将错误抛出
    }
}