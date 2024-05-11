import React from "react";
import { useEffect } from "react";
import { useRouter } from "next/router";

const Page = () => {
  const router = useRouter();
  const { slug } = router.query;
  console.log(slug);

  useEffect(() => {
    fetch(
      `http://127.0.0.1:5000/get_analysis/${slug[0]}/${slug[1]}`
    )
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  return <p>Post: {slug[0]}</p>;
};

export default Page;
