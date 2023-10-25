<script setup lang="ts">
import { ref } from 'vue'
import TheWelcome from '../components/TheWelcome.vue'
import axios from 'axios'
import saveAs from 'file-saver';

const urls = ref('') // 使用ref来创建响应式变量
const isLoading = ref(false)

const dealBlob = async function(res){
  // const blData = await res.blob()

  let url = window.URL.createObjectURL(new Blob([res], { type: 'application/vnd.ms-excel' }));
  let link = document.createElement('a');
  link.style.display = 'none';
  link.href = url;
  link.setAttribute('download', 'cookie-db' + '.xlsx');
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link); //下载完成移除元素
  window.URL.revokeObjectURL(url); //释放掉blob对象
}
const onSubmit = function(e){
  console.log(e);
  isLoading.value = true // 设置加载状态为true
  const path = 'http://localhost:5000/api/ping';
  axios({
    url: path, //用于请求的服务器 URL
    params: {
      urls: urls.value // 获取用户输入的URL字符串
    }, //必须是一个无格式对象(plain object)或 URLSearchParams 对象
    method: 'get', //请求时使用的方法,get默认
    responseType: 'blob', //表示服务器响应的数据类型，可以是 'arraybuffer', 'blob', 'document', 'json'(默认), 'text', 'stream'
  }).then((res) => {
      // 使用FileSaver.js保存二进制Blob为文件
      saveAs(new Blob([res.data], { type: 'application/vnd.ms-excel' }), 'cookie-db.xlsx');
  })
  .catch((error) => {
    // eslint-disable-next-line
    console.error(error);
  }).finally(() => {
    isLoading.value = false // 请求完成后设置加载状态为false
  });
}

</script>

<template>
  <main>
    <!-- <TheWelcome /> -->
    <h1>分析Cookie</h1>
    <div>
      <textarea v-model="urls" rows="10" style="width:800px" placeholder="请输入网址，以逗号分隔，如：https://www.baidu.com,https://www.163.com"/>
    </div>
    <div v-show="!urls" style="color:red">请输入网址</div>
    <div v-show="isLoading">分析中。。。</div>
    <div>
      <button :disabled="isLoading" @click="onSubmit">提交</button>
    </div>
  </main>
</template>
